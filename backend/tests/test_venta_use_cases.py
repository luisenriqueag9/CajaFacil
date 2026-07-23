import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.common.exceptions import ValidationException
from app.modules.venta.domain.entities.venta import Venta, DetalleVenta, FormaPagoAceptada
from app.modules.venta.domain.exceptions import (
    VentaVaciaException,
    CantidadInvalidaException,
    ImporteIncoherenteException,
    PagoInsuficienteException,
    ClienteRequeridoParaCreditoException,
    CajaCerradaException,
    VentaYaAnuladaException,
    VentaNotFoundException
)
from app.modules.venta.application.use_cases import (
    ConfirmarVentaUseCase,
    ConfirmarVentaCommand,
    DetalleVentaCommand,
    FormaPagoAceptadaCommand,
    AnularVentaUseCase,
    AnularVentaCommand,
    GetVentaByIdUseCase,
    ListSalesUseCase
)
from app.modules.venta.application.ports.product_lookup import ProductLookup
from app.modules.venta.application.ports.box_lookup import BoxLookup
from app.modules.venta.application.ports.credit_lookup import CreditLookup
from app.modules.venta.application.event_dispatcher import EventDispatcher
from app.modules.venta.domain.events.venta_events import VentaConfirmada, VentaAnulada

# ==========================================
# FAST IN-MEMORY REPOSITORY DOUBLES
# ==========================================

class InMemoryVentaRepository:
    def __init__(self):
        self.ventas = {}

    def save(self, venta: Venta) -> Venta:
        self.ventas[venta.id] = venta
        return venta

    def get_by_id(self, venta_id: uuid.UUID) -> Venta | None:
        return self.ventas.get(venta_id)

    def get_by_invoice_number(self, company_id: uuid.UUID, invoice_number: str) -> Venta | None:
        for v in self.ventas.values():
            if v.company_id == company_id and v.invoice_number == invoice_number:
                return v
        return None

    def search(self, company_id: uuid.UUID, filters: dict) -> list[Venta]:
        result = []
        for v in self.ventas.values():
            if v.company_id == company_id:
                if "box_id" in filters and filters["box_id"] and v.box_id != filters["box_id"]:
                    continue
                if "user_id" in filters and filters["user_id"] and v.user_id != filters["user_id"]:
                    continue
                if "client_id" in filters and filters["client_id"] and v.client_id != filters["client_id"]:
                    continue
                if "status" in filters and filters["status"] and v.status != filters["status"]:
                    continue
                result.append(v)
        return sorted(result, key=lambda x: x.created_at, reverse=True)


class DummyProductLookup(ProductLookup):
    def __init__(self, active_products: set[uuid.UUID]):
        self.active_products = active_products

    def exists_and_active(self, company_id: uuid.UUID, product_id: uuid.UUID) -> bool:
        return product_id in self.active_products


class DummyBoxLookup(BoxLookup):
    def __init__(self, open_boxes: set[uuid.UUID]):
        self.open_boxes = open_boxes

    def is_open_and_active(self, company_id: uuid.UUID, box_id: uuid.UUID) -> bool:
        return box_id in self.open_boxes


class DummyCreditLookup(CreditLookup):
    def __init__(self, active_credits: set[uuid.UUID]):
        self.active_credits = active_credits

    def has_active_credit_and_limit(self, company_id: uuid.UUID, client_id: uuid.UUID, required_amount: Decimal) -> bool:
        return client_id in self.active_credits


class DummySession:
    """Mock Session for SQLAlchemy during fast tests."""
    def begin_nested(self):
        class DummyNestedTrans:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
        return DummyNestedTrans()
    def commit(self): pass
    def rollback(self): pass


# ==========================================
# DOMIN INVARIANT TESTS
# ==========================================

def test_venta_domain_invariants():
    company_id = uuid.uuid4()
    box_id = uuid.uuid4()
    user_id = uuid.uuid4()
    client_id = uuid.uuid4()
    product_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # 1. Invariant: Venta Vacia (No details)
    with pytest.raises(VentaVaciaException):
        Venta(
            id=uuid.uuid4(),
            company_id=company_id,
            box_id=box_id,
            user_id=user_id,
            client_id=client_id,
            invoice_number="F-001",
            subtotal=Decimal("0.00"),
            discount=Decimal("0.00"),
            tax=Decimal("0.00"),
            total=Decimal("0.00"),
            status="CONFIRMADA",
            created_at=now,
            updated_at=now,
            details=[],
            payments=[FormaPagoAceptada(payment_method="EFECTIVO", amount=Decimal("0.00"))]
        )

    # 2. Invariant: Quantity > 0
    with pytest.raises(CantidadInvalidaException):
        Venta(
            id=uuid.uuid4(),
            company_id=company_id,
            box_id=box_id,
            user_id=user_id,
            client_id=client_id,
            invoice_number="F-001",
            subtotal=Decimal("100.00"),
            discount=Decimal("0.00"),
            tax=Decimal("15.00"),
            total=Decimal("115.00"),
            status="CONFIRMADA",
            created_at=now,
            updated_at=now,
            details=[
                DetalleVenta(
                    id=uuid.uuid4(),
                    product_id=product_id,
                    quantity=Decimal("0.00"), # Zero quantity
                    unit_price=Decimal("100.00"),
                    discount=Decimal("0.00"),
                    tax_rate=Decimal("0.15"),
                    tax_amount=Decimal("15.00"),
                    subtotal=Decimal("0.00"),
                    total=Decimal("0.00")
                )
            ],
            payments=[FormaPagoAceptada(payment_method="EFECTIVO", amount=Decimal("115.00"))]
        )

    # 3. Invariant: Coherencia de Cobertura Total del Importe
    with pytest.raises(PagoInsuficienteException):
        Venta(
            id=uuid.uuid4(),
            company_id=company_id,
            box_id=box_id,
            user_id=user_id,
            client_id=client_id,
            invoice_number="F-001",
            subtotal=Decimal("100.00"),
            discount=Decimal("0.00"),
            tax=Decimal("15.00"),
            total=Decimal("115.00"),
            status="CONFIRMADA",
            created_at=now,
            updated_at=now,
            details=[
                DetalleVenta(
                    id=uuid.uuid4(),
                    product_id=product_id,
                    quantity=Decimal("1.00"),
                    unit_price=Decimal("100.00"),
                    discount=Decimal("0.00"),
                    tax_rate=Decimal("0.15"),
                    tax_amount=Decimal("15.00"),
                    subtotal=Decimal("100.00"),
                    total=Decimal("115.00")
                )
            ],
            payments=[FormaPagoAceptada(payment_method="EFECTIVO", amount=Decimal("100.00"))] # 100 instead of 115
        )

    # 4. Invariant: Cliente Requerido para Credito
    with pytest.raises(ClienteRequeridoParaCreditoException):
        Venta(
            id=uuid.uuid4(),
            company_id=company_id,
            box_id=box_id,
            user_id=user_id,
            client_id=None, # Consumidor final
            invoice_number="F-001",
            subtotal=Decimal("100.00"),
            discount=Decimal("0.00"),
            tax=Decimal("15.00"),
            total=Decimal("115.00"),
            status="CONFIRMADA",
            created_at=now,
            updated_at=now,
            details=[
                DetalleVenta(
                    id=uuid.uuid4(),
                    product_id=product_id,
                    quantity=Decimal("1.00"),
                    unit_price=Decimal("100.00"),
                    discount=Decimal("0.00"),
                    tax_rate=Decimal("0.15"),
                    tax_amount=Decimal("15.00"),
                    subtotal=Decimal("100.00"),
                    total=Decimal("115.00")
                )
            ],
            payments=[FormaPagoAceptada(payment_method="CREDITO", amount=Decimal("115.00"))]
        )


# ==========================================
# USE CASE UNIT TESTS
# ==========================================

def test_confirmar_venta_happy_path():
    repo = InMemoryVentaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()
    
    company_id = uuid.uuid4()
    box_id = uuid.uuid4()
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()

    box_lookup = DummyBoxLookup({box_id})
    product_lookup = DummyProductLookup({product_id})
    credit_lookup = DummyCreditLookup(set())

    # Event spy
    published_events = []
    dispatcher.subscribe(VentaConfirmada, lambda ev: published_events.append(ev))

    use_case = ConfirmarVentaUseCase(
        repo, db, dispatcher, product_lookup, box_lookup, credit_lookup
    )

    command = ConfirmarVentaCommand(
        company_id=company_id,
        box_id=box_id,
        user_id=user_id,
        client_id=None,
        invoice_number="F-999",
        subtotal=Decimal("100.00"),
        discount=Decimal("0.00"),
        tax=Decimal("15.00"),
        total=Decimal("115.00"),
        details=[
            DetalleVentaCommand(
                product_id=product_id,
                quantity=Decimal("1.00"),
                unit_price=Decimal("100.00"),
                discount=Decimal("0.00"),
                tax_rate=Decimal("0.15"),
                tax_amount=Decimal("15.00"),
                subtotal=Decimal("100.00"),
                total=Decimal("115.00")
            )
        ],
        payments=[
            FormaPagoAceptadaCommand(
                payment_method="EFECTIVO",
                amount=Decimal("115.00")
            )
        ]
    )

    venta = use_case.execute(command)
    assert venta.status == "CONFIRMADA"
    assert venta.total == Decimal("115.00")
    assert repo.get_by_id(venta.id) is not None

    # Event verified
    assert len(published_events) == 1
    event = published_events[0]
    assert event.venta_id == venta.id
    assert event.total == Decimal("115.00")
    assert event.cash_amount == Decimal("115.00")
    assert event.credit_amount == Decimal("0.00")


def test_confirmar_venta_caja_cerrada_rejection():
    repo = InMemoryVentaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()
    
    company_id = uuid.uuid4()
    box_id = uuid.uuid4()
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()

    box_lookup = DummyBoxLookup(set()) # Empty, box closed
    product_lookup = DummyProductLookup({product_id})
    credit_lookup = DummyCreditLookup(set())

    use_case = ConfirmarVentaUseCase(
        repo, db, dispatcher, product_lookup, box_lookup, credit_lookup
    )

    command = ConfirmarVentaCommand(
        company_id=company_id,
        box_id=box_id,
        user_id=user_id,
        client_id=None,
        invoice_number="F-999",
        subtotal=Decimal("100.00"),
        discount=Decimal("0.00"),
        tax=Decimal("15.00"),
        total=Decimal("115.00"),
        details=[
            DetalleVentaCommand(
                product_id=product_id,
                quantity=Decimal("1.00"),
                unit_price=Decimal("100.00"),
                discount=Decimal("0.00"),
                tax_rate=Decimal("0.15"),
                tax_amount=Decimal("15.00"),
                subtotal=Decimal("100.00"),
                total=Decimal("115.00")
            )
        ],
        payments=[
            FormaPagoAceptadaCommand(
                payment_method="EFECTIVO",
                amount=Decimal("115.00")
            )
        ]
    )

    with pytest.raises(CajaCerradaException):
        use_case.execute(command)


def test_anular_venta_happy_path():
    repo = InMemoryVentaRepository()
    db = DummySession()
    dispatcher = EventDispatcher()
    
    company_id = uuid.uuid4()
    box_id = uuid.uuid4()
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    venta = Venta(
        id=uuid.uuid4(),
        company_id=company_id,
        box_id=box_id,
        user_id=user_id,
        client_id=None,
        invoice_number="F-888",
        subtotal=Decimal("100.00"),
        discount=Decimal("0.00"),
        tax=Decimal("15.00"),
        total=Decimal("115.00"),
        status="CONFIRMADA",
        created_at=now,
        updated_at=now,
        details=[
            DetalleVenta(
                id=uuid.uuid4(),
                product_id=product_id,
                quantity=Decimal("1.00"),
                unit_price=Decimal("100.00"),
                discount=Decimal("0.00"),
                tax_rate=Decimal("0.15"),
                tax_amount=Decimal("15.00"),
                subtotal=Decimal("100.00"),
                total=Decimal("115.00")
            )
        ],
        payments=[
            FormaPagoAceptada(
                payment_method="EFECTIVO",
                amount=Decimal("115.00")
            )
        ]
    )
    repo.save(venta)

    published_events = []
    dispatcher.subscribe(VentaAnulada, lambda ev: published_events.append(ev))

    use_case = AnularVentaUseCase(repo, db, dispatcher)
    supervisor_id = uuid.uuid4()
    command = AnularVentaCommand(
        venta_id=venta.id,
        supervisor_id=supervisor_id,
        reason="Error de digitación en caja"
    )

    annulled = use_case.execute(command)
    assert annulled.status == "ANULADA"
    assert annulled.voided_by == supervisor_id
    assert annulled.void_reason == "Error de digitación en caja"

    # Event verified
    assert len(published_events) == 1
    event = published_events[0]
    assert event.venta_id == venta.id
    assert event.voided_by == supervisor_id
    assert event.void_reason == "Error de digitación en caja"


# ==========================================
# SQLALCHEMY INTEGRATION & ROLLBACK TESTS
# ==========================================

def test_unit_of_work_transactional_rollback():
    # 1. Setup in-memory SQLite database using SQLAlchemy Base metadata
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db_session = TestingSessionLocal()

    try:
        from app.modules.venta.data.repositories.venta_repository_impl import VentaRepositoryImpl
        from app.modules.venta.data.repositories.mock_repositories import (
            MockMovimientoInventarioRepositoryImpl,
            MockMovimientoCajaRepositoryImpl,
            MockCreditoRepositoryImpl
        )
        from app.modules.venta.application.handlers.venta_confirmada_handlers import VentaEventHandler
        from app.modules.venta.data.models import Venta as DBVenta, DBMovimientoInventario

        # 2. Setup concrete infrastructure dependencies using the testing DB session
        venta_repo = VentaRepositoryImpl(db_session)
        inv_repo = MockMovimientoInventarioRepositoryImpl(db_session)
        caja_repo = MockMovimientoCajaRepositoryImpl(db_session)
        cred_repo = MockCreditoRepositoryImpl(db_session)

        # 3. Setup dispatcher and subscribe handler
        dispatcher = EventDispatcher()
        handler = VentaEventHandler(inv_repo, caja_repo, cred_repo)
        dispatcher.subscribe(VentaConfirmada, handler.handle_confirmada)

        # 4. Injected lookups (Always True for this database test)
        class DirectProductLookup(ProductLookup):
            def exists_and_active(self, company_id, product_id): return True
        class DirectBoxLookup(BoxLookup):
            def is_open_and_active(self, company_id, box_id): return True
        class DirectCreditLookup(CreditLookup):
            def has_active_credit_and_limit(self, company_id, client_id, required_amount): return True

        # 5. Build ConfirmarVentaUseCase
        use_case = ConfirmarVentaUseCase(
            repository=venta_repo,
            db=db_session,
            event_dispatcher=dispatcher,
            product_lookup=DirectProductLookup(),
            box_lookup=DirectBoxLookup(),
            credit_lookup=DirectCreditLookup()
        )

        company_id = uuid.uuid4()
        box_id = uuid.uuid4()
        user_id = uuid.uuid4()
        product_id = uuid.uuid4()

        command = ConfirmarVentaCommand(
            company_id=company_id,
            box_id=box_id,
            user_id=user_id,
            client_id=None,
            invoice_number="FACT-TEST-ROLLBACK",
            subtotal=Decimal("100.00"),
            discount=Decimal("0.00"),
            tax=Decimal("15.00"),
            total=Decimal("115.00"),
            details=[
                DetalleVentaCommand(
                    product_id=product_id,
                    quantity=Decimal("1.00"),
                    unit_price=Decimal("100.00"),
                    discount=Decimal("0.00"),
                    tax_rate=Decimal("0.15"),
                    tax_amount=Decimal("15.00"),
                    subtotal=Decimal("100.00"),
                    total=Decimal("115.00")
                )
            ],
            payments=[
                FormaPagoAceptadaCommand(
                    payment_method="EFECTIVO",
                    amount=Decimal("115.00")
                )
            ]
        )

        # 6. FORCE AN EXCEPTION inside one of the event handlers to trigger rollback.
        # We can mock the inv_repo.registrar_movimiento to raise a ValueError.
        original_registrar_movimiento = inv_repo.registrar_movimiento
        
        def failing_registrar_movimiento(*args, **kwargs):
            raise ValueError("Forced error in inventory handler to test database rollback!")
            
        inv_repo.registrar_movimiento = failing_registrar_movimiento

        # 7. Execute use case and expect ValueError
        with pytest.raises(ValueError, match="Forced error in inventory handler"):
            use_case.execute(command)

        # 8. VERIFY ROLLBACK: Check that absolutely nothing was committed to SQLite database!
        # There should be NO Venta records and NO MovimientoInventario records in the database.
        db_session.close() # Close session to clear any cache
        db_session = TestingSessionLocal()
        
        ventas_in_db = db_session.query(DBVenta).all()
        inventory_moves_in_db = db_session.query(DBMovimientoInventario).all()

        assert len(ventas_in_db) == 0, "The sale should have been rolled back and not persisted!"
        assert len(inventory_moves_in_db) == 0, "The inventory movement should have been rolled back and not persisted!"

    finally:
        db_session.close()
