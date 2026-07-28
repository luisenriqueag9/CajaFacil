import pytest
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.modules.compra.domain.entities.compra import Compra
from app.modules.compra.domain.entities.detalle_compra import DetalleCompra
from app.modules.compra.domain.exceptions import CompraNoEncontradaException, CompraYaExisteException, CompraInvalidaException
from app.modules.compra.application.ports.supplier_lookup import SupplierLookup
from app.modules.compra.application.ports.product_lookup import ProductLookup
from app.modules.compra.domain.events.compra_events import CompraRegistrada, CompraAnulada
from app.common.event_dispatcher import EventDispatcher
from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.application.use_cases import (
    RegistrarCompraUseCase,
    RegistrarCompraCommand,
    DetalleCompraCommand,
    AnularCompraUseCase,
    AnularCompraCommand,
    ObtenerCompraPorIdUseCase,
    ListarComprasUseCase,
)

class InMemoryCompraRepository(CompraRepository):
    def __init__(self):
        self.purchases = {}

    def create(self, compra: Compra) -> Compra:
        self.purchases[compra.id] = compra
        return compra

    def get_by_id(self, purchase_id: uuid.UUID) -> Compra | None:
        return self.purchases.get(purchase_id)

    def get_by_invoice_number(self, company_id: uuid.UUID, supplier_id: uuid.UUID, invoice_number: str) -> Compra | None:
        for p in self.purchases.values():
            if p.company_id == company_id and p.supplier_id == supplier_id and p.invoice_number.lower() == invoice_number.lower():
                return p
        return None

    def get_all(self, company_id: uuid.UUID, status: str | None = None, supplier_id: uuid.UUID | None = None) -> list[Compra]:
        result = []
        for p in self.purchases.values():
            if p.company_id == company_id:
                if status and p.status != status:
                    continue
                if supplier_id and p.supplier_id != supplier_id:
                    continue
                result.append(p)
        return sorted(result, key=lambda x: x.created_at, reverse=True)

    def update(self, compra: Compra) -> Compra:
        self.purchases[compra.id] = compra
        return compra


class DummySupplierLookup(SupplierLookup):
    def __init__(self, active_suppliers: set[uuid.UUID]):
        self.active_suppliers = active_suppliers

    def exists_and_active(self, company_id: uuid.UUID, supplier_id: uuid.UUID) -> bool:
        return supplier_id in self.active_suppliers


class DummyProductLookup(ProductLookup):
    def __init__(self, active_products: set[uuid.UUID]):
        self.active_products = active_products

    def exists_and_active(self, company_id: uuid.UUID, product_id: uuid.UUID) -> bool:
        return product_id in self.active_products


class SpyEventDispatcher(EventDispatcher):
    def __init__(self):
        self.dispatched_events = []

    def dispatch(self, event: object) -> None:
        self.dispatched_events.append(event)


@pytest.fixture
def db_session_mock():
    mock = MagicMock(spec=Session)
    # Configure context manager for begin_nested()
    nested_mock = MagicMock()
    mock.begin_nested.return_value = nested_mock
    return mock


def test_purchase_registration_happy_path(db_session_mock):
    repo = InMemoryCompraRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()
    product2 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1, product2})
    spy_dispatcher = SpyEventDispatcher()

    use_case = RegistrarCompraUseCase(
        repo, 
        db_session_mock, 
        supplier_lookup, 
        product_lookup, 
        spy_dispatcher
    )

    items_command = [
        DetalleCompraCommand(product_id=product1, quantity=Decimal("10.00"), unit_cost=Decimal("25.50")),
        DetalleCompraCommand(product_id=product2, quantity=Decimal("5.00"), unit_cost=Decimal("100.00"))
    ]

    command = RegistrarCompraCommand(
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-001",
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        items=items_command
    )

    created = use_case.execute(command)
    assert created.status == "REGISTRADA"
    assert created.subtotal == Decimal("255.00") + Decimal("500.00")
    assert created.total == Decimal("755.00")
    assert len(created.items) == 2

    # Verify event dispatched (1 CompraRegistrada)
    assert len(spy_dispatcher.dispatched_events) == 1
    event = spy_dispatcher.dispatched_events[0]
    assert isinstance(event, CompraRegistrada)
    assert event.purchase_id == created.id
    assert event.total == Decimal("755.00")
    assert len(event.items) == 2


def test_purchase_v1_consolidation_policy(db_session_mock):
    repo = InMemoryCompraRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1})
    spy_dispatcher = SpyEventDispatcher()

    use_case = RegistrarCompraUseCase(
        repo, 
        db_session_mock, 
        supplier_lookup, 
        product_lookup, 
        spy_dispatcher
    )

    # Registering with duplicate product entries: 10 units at 20.0, and 10 units at 30.0
    items_command = [
        DetalleCompraCommand(product_id=product1, quantity=Decimal("10.00"), unit_cost=Decimal("20.00")),
        DetalleCompraCommand(product_id=product1, quantity=Decimal("10.00"), unit_cost=Decimal("30.00"))
    ]

    command = RegistrarCompraCommand(
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-002",
        payment_condition="CREDITO",
        issue_date=datetime.now(timezone.utc),
        items=items_command
    )

    created = use_case.execute(command)
    
    # Should consolidate duplicate product entries into 1 detail line (RN-307)
    assert len(created.items) == 1
    consolidated_item = created.items[0]
    assert consolidated_item.quantity == Decimal("20.00")
    assert consolidated_item.unit_cost == Decimal("25.00")  # Weighted average cost: (10*20 + 10*30)/20 = 25.0
    assert created.total == Decimal("500.00")


def test_purchase_duplicate_invoice_rejection(db_session_mock):
    repo = InMemoryCompraRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1})
    spy_dispatcher = SpyEventDispatcher()

    use_case = RegistrarCompraUseCase(
        repo, 
        db_session_mock, 
        supplier_lookup, 
        product_lookup, 
        spy_dispatcher
    )

    items_command = [DetalleCompraCommand(product_id=product1, quantity=Decimal("1.00"), unit_cost=Decimal("10.00"))]

    c1 = RegistrarCompraCommand(
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-123",
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        items=items_command
    )
    use_case.execute(c1)

    c2 = RegistrarCompraCommand(
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-123",  # duplicate invoice number
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        items=items_command
    )

    with pytest.raises(CompraYaExisteException):
        use_case.execute(c2)


def test_purchase_domain_invariants():
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    # Invariant: quantity > 0
    with pytest.raises(CompraInvalidaException):
        Compra.register(
            id=uuid.uuid4(),
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number="FACT-INV",
            payment_condition="CONTADO",
            issue_date=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            items_payload=[{"product_id": product1, "quantity": Decimal("0.00"), "unit_cost": Decimal("10.00")}]
        )

    # Invariant: unit_cost >= 0
    with pytest.raises(CompraInvalidaException):
        Compra.register(
            id=uuid.uuid4(),
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number="FACT-INV",
            payment_condition="CONTADO",
            issue_date=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            items_payload=[{"product_id": product1, "quantity": Decimal("5.00"), "unit_cost": Decimal("-1.00")}]
        )

    # Invariant: Registered purchase cannot be created without items
    with pytest.raises(CompraInvalidaException):
        Compra.register(
            id=uuid.uuid4(),
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number="FACT-INV",
            payment_condition="CONTADO",
            issue_date=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            items_payload=[]
        )


def test_purchase_annulment_state_change(db_session_mock):
    repo = InMemoryCompraRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1})
    spy_dispatcher = SpyEventDispatcher()

    reg_use_case = RegistrarCompraUseCase(
        repo, 
        db_session_mock, 
        supplier_lookup, 
        product_lookup, 
        spy_dispatcher
    )
    annul_use_case = AnularCompraUseCase(repo, db_session_mock, spy_dispatcher)

    items_command = [DetalleCompraCommand(product_id=product1, quantity=Decimal("1.00"), unit_cost=Decimal("10.00"))]
    command = RegistrarCompraCommand(
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-ANN",
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        items=items_command
    )
    
    created = reg_use_case.execute(command)
    assert created.status == "REGISTRADA"

    annul_command = AnularCompraCommand(purchase_id=created.id, void_reason="Motivo test")
    annulled = annul_use_case.execute(annul_command)
    assert annulled.status == "ANULADA"
    assert repo.get_by_id(created.id).status == "ANULADA"

    # Verify event dispatched (CompraRegistrada + CompraAnulada)
    assert len(spy_dispatcher.dispatched_events) == 2
    assert isinstance(spy_dispatcher.dispatched_events[1], CompraAnulada)
    assert spy_dispatcher.dispatched_events[1].purchase_id == created.id
