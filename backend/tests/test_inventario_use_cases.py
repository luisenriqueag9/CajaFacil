import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario, Merma, AjusteInventario
from app.modules.inventario.domain.exceptions import (
    CantidadInvalidaException,
    StockInsuficienteException,
    ProductoNoManejaInventarioException
)
from app.modules.inventario.application.use_cases import (
    RegistrarMovimientoUseCase,
    RegistrarMovimientoCommand,
    RegistrarMermaUseCase,
    RegistrarMermaCommand,
    RegistrarAjusteUseCase,
    RegistrarAjusteCommand,
    ObtenerStockProductoUseCase,
    ListarMovimientosUseCase
)
from app.modules.inventario.application.ports.product_lookup import ProductLookup, ProductDetails
from app.modules.inventario.application.event_dispatcher import EventDispatcher
from app.modules.inventario.domain.events.inventario_events import (
    InventarioActualizado,
    MermaRegistrada,
    AjusteInventarioRegistrado
)

# ==========================================
# FAST IN-MEMORY REPOSITORY DOUBLE
# ==========================================

class InMemoryMovimientoRepository:
    def __init__(self):
        self.movements = {}

    def save(self, movimiento: MovimientoInventario) -> MovimientoInventario:
        self.movements[movimiento.id] = movimiento
        return movimiento

    def get_by_id(self, movimiento_id: uuid.UUID) -> MovimientoInventario | None:
        return self.movements.get(movimiento_id)

    def get_by_product_id(self, company_id: uuid.UUID, product_id: uuid.UUID) -> list[MovimientoInventario]:
        result = []
        for m in self.movements.values():
            if m.company_id == company_id and m.product_id == product_id:
                result.append(m)
        return sorted(result, key=lambda x: x.created_at)

    def search(self, company_id: uuid.UUID, filters: dict) -> list[MovimientoInventario]:
        result = []
        for m in self.movements.values():
            if m.company_id == company_id:
                if "product_id" in filters and filters["product_id"] and m.product_id != filters["product_id"]:
                    continue
                if "type" in filters and filters["type"] and m.type != filters["type"]:
                    continue
                if "concept" in filters and filters["concept"] and m.concept != filters["concept"]:
                    continue
                result.append(m)
        return sorted(result, key=lambda x: x.created_at, reverse=True)


class DummyProductLookup(ProductLookup):
    def __init__(self, products_map: dict):
        self.products_map = products_map

    def get_details(self, company_id: uuid.UUID, product_id: uuid.UUID) -> ProductDetails:
        return self.products_map.get(
            product_id,
            ProductDetails(exists=False, active=False, controls_stock=False, allows_negative=False)
        )


class DummySession:
    def begin_nested(self):
        class DummyNestedTrans:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
        return DummyNestedTrans()
    def commit(self): pass
    def rollback(self): pass


# ==========================================
# DOMAIN INVARIANT TESTS
# ==========================================

def test_inventario_domain_invariants():
    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # 1. Invariant: Cantidad <= 0
    with pytest.raises(CantidadInvalidaException):
        MovimientoInventario(
            id=uuid.uuid4(),
            company_id=company_id,
            product_id=product_id,
            type="ENTRADA",
            concept="COMPRA",
            quantity=Decimal("0.00"),
            origin_document_id=None,
            created_at=now,
            created_by=user_id
        )

    # 2. Invariant: MERMA requires Merma entity
    with pytest.raises(ValueError, match="incluir su entidad de detalle Merma"):
        MovimientoInventario(
            id=uuid.uuid4(),
            company_id=company_id,
            product_id=product_id,
            type="SALIDA",
            concept="MERMA",
            quantity=Decimal("10.00"),
            origin_document_id=None,
            created_at=now,
            created_by=user_id,
            merma=None
        )

    # 3. Invariant: AJUSTE requires AjusteInventario entity
    with pytest.raises(ValueError, match="incluir su entidad de detalle AjusteInventario"):
        MovimientoInventario(
            id=uuid.uuid4(),
            company_id=company_id,
            product_id=product_id,
            type="SALIDA",
            concept="AJUSTE",
            quantity=Decimal("5.00"),
            origin_document_id=None,
            created_at=now,
            created_by=user_id,
            ajuste=None
        )


# ==========================================
# USE CASE UNIT TESTS
# ==========================================

def test_registrar_movimiento_happy_path():
    repo = InMemoryMovimientoRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()

    product_lookup = DummyProductLookup({
        product_id: ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)
    })

    published_events = []
    dispatcher.subscribe(InventarioActualizado, lambda ev: published_events.append(ev))

    use_case = RegistrarMovimientoUseCase(repo, db, dispatcher, product_lookup)

    # Register ENTRADA movement
    command = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=product_id,
        type="ENTRADA",
        concept="INVENTARIO_INICIAL",
        quantity=Decimal("50.00"),
        created_by=user_id
    )

    mov = use_case.execute(command)
    assert mov.type == "ENTRADA"
    assert mov.quantity == Decimal("50.00")
    assert len(published_events) == 1
    assert published_events[0].new_balance == Decimal("50.00")


def test_registrar_movimiento_insufficient_stock():
    repo = InMemoryMovimientoRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()

    product_lookup = DummyProductLookup({
        product_id: ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)
    })

    use_case = RegistrarMovimientoUseCase(repo, db, dispatcher, product_lookup)

    # Try SALIDA without initial stock (should fail as allows_negative is False)
    command = RegistrarMovimientoCommand(
        company_id=company_id,
        product_id=product_id,
        type="SALIDA",
        concept="VENTA",
        quantity=Decimal("5.00"),
        created_by=user_id
    )

    with pytest.raises(StockInsuficienteException):
        use_case.execute(command)


def test_registrar_merma_happy_path():
    repo = InMemoryMovimientoRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()

    product_lookup = DummyProductLookup({
        product_id: ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)
    })

    # Register initial stock first
    initial_mov = MovimientoInventario(
        id=uuid.uuid4(),
        company_id=company_id,
        product_id=product_id,
        type="ENTRADA",
        concept="INVENTARIO_INICIAL",
        quantity=Decimal("20.00"),
        origin_document_id=None,
        created_at=datetime.now(timezone.utc),
        created_by=user_id
    )
    repo.save(initial_mov)

    published_events = []
    dispatcher.subscribe(MermaRegistrada, lambda ev: published_events.append(ev))
    dispatcher.subscribe(InventarioActualizado, lambda ev: published_events.append(ev))

    use_case = RegistrarMermaUseCase(repo, db, dispatcher, product_lookup)

    command = RegistrarMermaCommand(
        company_id=company_id,
        product_id=product_id,
        quantity=Decimal("3.00"),
        reason="ROTURA",
        created_by=user_id,
        description="Botella de vidrio rota durante limpieza"
    )

    mov = use_case.execute(command)
    assert mov.concept == "MERMA"
    assert mov.merma is not None
    assert mov.merma.reason == "ROTURA"
    assert mov.merma.description == "Botella de vidrio rota durante limpieza"

    # Verify event published (2 events: Update + Merma)
    assert len(published_events) == 2
    assert any(isinstance(ev, MermaRegistrada) for ev in published_events)


def test_registrar_ajuste_happy_path():
    repo = InMemoryMovimientoRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()

    product_lookup = DummyProductLookup({
        product_id: ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)
    })

    # System stock is currently 10
    initial_mov = MovimientoInventario(
        id=uuid.uuid4(),
        company_id=company_id,
        product_id=product_id,
        type="ENTRADA",
        concept="INVENTARIO_INICIAL",
        quantity=Decimal("10.00"),
        origin_document_id=None,
        created_at=datetime.now(timezone.utc),
        created_by=user_id
    )
    repo.save(initial_mov)

    published_events = []
    dispatcher.subscribe(AjusteInventarioRegistrado, lambda ev: published_events.append(ev))

    use_case = RegistrarAjusteUseCase(repo, db, dispatcher, product_lookup)

    # Physical count is 15 (excedente of 5)
    command = RegistrarAjusteCommand(
        company_id=company_id,
        product_id=product_id,
        physical_quantity=Decimal("15.00"),
        supervisor_id=user_id,
        notes="Ajuste anual de auditoria"
    )

    mov = use_case.execute(command)
    assert mov.type == "ENTRADA"
    assert mov.quantity == Decimal("5.00")
    assert mov.ajuste.difference == Decimal("5.00")
    assert mov.ajuste.system_quantity == Decimal("10.00")

    # Verify event published
    assert len(published_events) == 1
    assert published_events[0].difference == Decimal("5.00")


# ==========================================
# SQLALCHEMY INTEGRATION & ROLLBACK TESTS
# ==========================================

def test_inventario_transactional_rollback():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db_session = TestingSessionLocal()

    try:
        from app.modules.inventario.data.repositories.movimiento_repository_impl import MovimientoInventarioRepositoryImpl
        from app.modules.inventario.data.models import MovimientoInventario as DBMovimiento

        # Setup concrete infra repositories
        repo = MovimientoInventarioRepositoryImpl(db_session)
        dispatcher = EventDispatcher()

        # Injected stub lookups
        class DirectProductLookup(ProductLookup):
            def get_details(self, company_id, product_id):
                return ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)

        # Force exception on dispatcher subscription to trigger rollback
        def failing_subscriber(ev):
            raise RuntimeError("Forced failure in listener to trigger database rollback!")

        dispatcher.subscribe(InventarioActualizado, failing_subscriber)

        use_case = RegistrarMovimientoUseCase(
            repository=repo,
            db=db_session,
            event_dispatcher=dispatcher,
            product_lookup=DirectProductLookup()
        )

        company_id = uuid.uuid4()
        product_id = uuid.uuid4()
        user_id = uuid.uuid4()

        command = RegistrarMovimientoCommand(
            company_id=company_id,
            product_id=product_id,
            type="ENTRADA",
            concept="INVENTARIO_INICIAL",
            quantity=Decimal("100.00"),
            created_by=user_id
        )

        with pytest.raises(RuntimeError, match="Forced failure in listener"):
            use_case.execute(command)

        # Check DB: session close and re-fetch should show NO movements registered
        db_session.close()
        db_session = TestingSessionLocal()

        movs_in_db = db_session.query(DBMovimiento).all()
        assert len(movs_in_db) == 0, "Database should have rolled back completely!"

    finally:
        db_session.close()
