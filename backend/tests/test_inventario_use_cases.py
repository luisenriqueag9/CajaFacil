import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario, Merma, AjusteInventario
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto
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
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
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


class InMemoryExistenciaRepository(ExistenciaRepository):
    def __init__(self):
        self.existencias = {}

    def save(self, existencia: ExistenciaProducto) -> ExistenciaProducto:
        self.existencias[(existencia.company_id, existencia.product_id)] = existencia
        return existencia

    def get_by_product_id(self, company_id: uuid.UUID, product_id: uuid.UUID) -> ExistenciaProducto | None:
        return self.existencias.get((company_id, product_id))

    def search(self, company_id: uuid.UUID, filters: dict) -> list[ExistenciaProducto]:
        return list(self.existencias.values())


class DummySession:
    def begin_nested(self):
        class DummyNestedTrans:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
        return DummyNestedTrans()
    def commit(self): pass
    def rollback(self): pass


class DummyProductLookup(ProductLookup):
    def __init__(self, products_dict):
        self.products = products_dict

    def get_details(self, company_id: uuid.UUID, product_id: uuid.UUID) -> ProductDetails:
        return self.products.get(product_id, ProductDetails(exists=False, active=False, controls_stock=False, allows_negative=False))


# ==========================================
# DOMAIN ENTITY TESTS
# ==========================================

def test_movimiento_inventario_entity_validation():
    # 1. Invalid concept value
    with pytest.raises(ValueError, match="Concepto de movimiento inválido"):
        MovimientoInventario(
            id=uuid.uuid4(),
            company_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            type="ENTRADA",
            concept="VENTA_MALA",
            quantity=Decimal("10.00"),
            origin_document_id=None,
            created_at=datetime.now(timezone.utc),
            created_by=uuid.uuid4()
        )

    # 2. Invalid negative quantity
    with pytest.raises(CantidadInvalidaException):
        MovimientoInventario(
            id=uuid.uuid4(),
            company_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            type="SALIDA",
            concept="VENTA",
            quantity=Decimal("-2.00"),
            origin_document_id=None,
            created_at=datetime.now(timezone.utc),
            created_by=uuid.uuid4()
        )

    # 3. Missing Merma detail for MERMA concept
    with pytest.raises(ValueError, match="debe incluir su entidad de detalle Merma"):
        MovimientoInventario(
            id=uuid.uuid4(),
            company_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            type="SALIDA",
            concept="MERMA",
            quantity=Decimal("1.00"),
            origin_document_id=None,
            created_at=datetime.now(timezone.utc),
            created_by=uuid.uuid4()
        )


# ==========================================
# USE CASE UNIT TESTS
# ==========================================

def test_registrar_movimiento_happy_path():
    repo = InMemoryMovimientoRepository()
    existencia_repo = InMemoryExistenciaRepository()
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

    use_case = RegistrarMovimientoUseCase(repo, existencia_repo, db, dispatcher, product_lookup)

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
    existencia_repo = InMemoryExistenciaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()

    product_lookup = DummyProductLookup({
        product_id: ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)
    })

    use_case = RegistrarMovimientoUseCase(repo, existencia_repo, db, dispatcher, product_lookup)

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
    existencia_repo = InMemoryExistenciaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()

    company_id = uuid.uuid4()
    product_id = uuid.uuid4()
    user_id = uuid.uuid4()

    product_lookup = DummyProductLookup({
        product_id: ProductDetails(exists=True, active=True, controls_stock=True, allows_negative=False)
    })

    # Register initial stock in both movement and existence repo
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
    existencia_repo.save(ExistenciaProducto(
        id=uuid.uuid4(),
        company_id=company_id,
        product_id=product_id,
        stock=Decimal("20.00")
    ))

    published_events = []
    dispatcher.subscribe(MermaRegistrada, lambda ev: published_events.append(ev))
    dispatcher.subscribe(InventarioActualizado, lambda ev: published_events.append(ev))

    use_case = RegistrarMermaUseCase(repo, existencia_repo, db, dispatcher, product_lookup)

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
    existencia_repo = InMemoryExistenciaRepository()
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
    existencia_repo.save(ExistenciaProducto(
        id=uuid.uuid4(),
        company_id=company_id,
        product_id=product_id,
        stock=Decimal("10.00")
    ))

    published_events = []
    dispatcher.subscribe(AjusteInventarioRegistrado, lambda ev: published_events.append(ev))

    use_case = RegistrarAjusteUseCase(repo, existencia_repo, db, dispatcher, product_lookup)

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
    from app.modules.company.data.models import Company
    from app.modules.product.data.models import Product
    from app.modules.brand.data.models import Brand
    from app.modules.category.data.models import Category

    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db_session = TestingSessionLocal()

    try:
        from app.modules.inventario.data.repositories.movimiento_repository_impl import MovimientoInventarioRepositoryImpl
        from app.modules.inventario.data.repositories.existencia_repository_impl import ExistenciaRepositoryImpl
        from app.modules.inventario.data.models import MovimientoInventario as DBMovimiento

        # Pre-populate required company and products to satisfy FK constraints in sqlite
        comp_id = uuid.UUID("11111111-1111-1111-1111-11111111111a")
        prod_id = uuid.UUID("22222222-2222-2222-2222-22222222222b")

        from app.modules.unit.data.models import Unit

        db_session.add(Company(
            id=comp_id,
            business_name="Empresa Test",
            trade_name="Empresa Test",
            tax_id="12345678-9",
            email="test@empresa.com",
            currency="USD",
            timezone="UTC",
            status="ACTIVE"
        ))
        brand = Brand(id=uuid.uuid4(), company_id=comp_id, name="Marca Test")
        cat = Category(id=uuid.uuid4(), company_id=comp_id, name="Categoria Test")
        unit = Unit(id=uuid.uuid4(), company_id=comp_id, code="UN01", name="Unidad", abbreviation="UN", allows_decimal=False, status="ACTIVE")
        db_session.add(brand)
        db_session.add(cat)
        db_session.add(unit)
        db_session.flush()

        db_session.add(Product(
            id=prod_id, company_id=comp_id, name="Refresco", internal_code="REF01",
            cost=Decimal("10.00"), price=Decimal("15.00"), tax_rate=Decimal("15.00"), status="ACTIVE",
            controls_stock=True, allows_decimal=False, minimum_stock=Decimal("5.00"),
            brand_id=brand.id, category_id=cat.id, unit_id=unit.id
        ))
        db_session.commit()

        # Setup concrete infra repositories
        repo = MovimientoInventarioRepositoryImpl(db_session)
        existencia_repo = ExistenciaRepositoryImpl(db_session)
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
            existencia_repository=existencia_repo,
            db=db_session,
            event_dispatcher=dispatcher,
            product_lookup=DirectProductLookup()
        )

        command = RegistrarMovimientoCommand(
            company_id=comp_id,
            product_id=prod_id,
            type="ENTRADA",
            concept="INVENTARIO_INICIAL",
            quantity=Decimal("100.00"),
            created_by=uuid.uuid4()
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
