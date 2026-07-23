import pytest
import uuid
from datetime import datetime, timezone
from app.modules.purchase.domain.entities.purchase import Purchase
from app.modules.purchase.domain.entities.purchase_detail import PurchaseDetail
from app.modules.purchase.domain.exceptions import PurchaseNotFoundException, PurchaseAlreadyExistsException, InvalidPurchaseException
from app.modules.purchase.application.ports.supplier_lookup import SupplierLookup
from app.modules.purchase.application.ports.product_lookup import ProductLookup
from app.modules.purchase.application.ports.event_publisher import EventPublisher
from app.modules.purchase.application.events.purchase_events import PurchaseConfirmedEvent, PurchaseAnnulledEvent
from app.modules.purchase.application.use_cases import (
    RegisterPurchaseUseCase,
    AnnulPurchaseUseCase,
    GetPurchaseByIdUseCase,
    ListPurchasesUseCase,
)

class InMemoryPurchaseRepository:
    def __init__(self):
        self.purchases = {}

    def create(self, purchase: Purchase) -> Purchase:
        self.purchases[purchase.id] = purchase
        return purchase

    def get_by_id(self, purchase_id: uuid.UUID) -> Purchase | None:
        return self.purchases.get(purchase_id)

    def get_by_invoice_number(self, company_id: uuid.UUID, supplier_id: uuid.UUID, invoice_number: str) -> Purchase | None:
        for p in self.purchases.values():
            if p.company_id == company_id and p.supplier_id == supplier_id and p.invoice_number.lower() == invoice_number.lower():
                return p
        return None

    def get_all(self, company_id: uuid.UUID, status: str | None = None, supplier_id: uuid.UUID | None = None) -> list[Purchase]:
        result = []
        for p in self.purchases.values():
            if p.company_id == company_id:
                if status and p.status != status:
                    continue
                if supplier_id and p.supplier_id != supplier_id:
                    continue
                result.append(p)
        return sorted(result, key=lambda x: x.created_at, reverse=True)

    def update(self, purchase: Purchase) -> Purchase:
        self.suppliers = self.purchases[purchase.id] = purchase
        return purchase


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


class SpyEventPublisher(EventPublisher):
    def __init__(self):
        self.published_events = []

    def publish(self, event: object) -> None:
        self.published_events.append(event)


def test_purchase_registration_happy_path():
    repo = InMemoryPurchaseRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()
    product2 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1, product2})
    spy_publisher = SpyEventPublisher()

    use_case = RegisterPurchaseUseCase(repo, supplier_lookup, product_lookup, spy_publisher)

    items_payload = [
        {"product_id": product1, "quantity": 10.0, "unit_cost": 25.5},
        {"product_id": product2, "quantity": 5.0, "unit_cost": 100.0}
    ]

    purchase_id = uuid.uuid4()
    purchase = Purchase.register(
        id=purchase_id,
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-001",
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        items_payload=items_payload
    )

    created = use_case.execute(purchase)
    assert created.status == "CONFIRMADA"
    assert created.subtotal == 255.0 + 500.0
    assert created.total == 755.0
    assert len(created.items) == 2

    # Verify event published
    assert len(spy_publisher.published_events) == 1
    event = spy_publisher.published_events[0]
    assert isinstance(event, PurchaseConfirmedEvent)
    assert event.purchase_id == purchase_id
    assert event.total == 755.0
    assert len(event.items) == 2


def test_purchase_v1_consolidation_policy():
    repo = InMemoryPurchaseRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1})
    spy_publisher = SpyEventPublisher()

    use_case = RegisterPurchaseUseCase(repo, supplier_lookup, product_lookup, spy_publisher)

    # Registering with duplicate product entries: 10 units at 20.0, and 10 units at 30.0
    items_payload = [
        {"product_id": product1, "quantity": 10.0, "unit_cost": 20.0},
        {"product_id": product1, "quantity": 10.0, "unit_cost": 30.0}
    ]

    purchase = Purchase.register(
        id=uuid.uuid4(),
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-002",
        payment_condition="CREDITO",
        issue_date=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        items_payload=items_payload
    )

    created = use_case.execute(purchase)
    
    # Should consolidate duplicate product entries into 1 detail line
    assert len(created.items) == 1
    consolidated_item = created.items[0]
    assert consolidated_item.quantity == 20.0
    assert consolidated_item.unit_cost == 25.0  # Weighted average cost: (10*20 + 10*30)/20 = 25.0
    assert created.total == 500.0


def test_purchase_duplicate_invoice_rejection():
    repo = InMemoryPurchaseRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1})
    spy_publisher = SpyEventPublisher()

    use_case = RegisterPurchaseUseCase(repo, supplier_lookup, product_lookup, spy_publisher)

    items_payload = [{"product_id": product1, "quantity": 1.0, "unit_cost": 10.0}]

    p1 = Purchase.register(
        id=uuid.uuid4(),
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-123",
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        items_payload=items_payload
    )
    use_case.execute(p1)

    p2 = Purchase.register(
        id=uuid.uuid4(),
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-123",  # duplicate invoice number for the same supplier
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        items_payload=items_payload
    )

    with pytest.raises(PurchaseAlreadyExistsException):
        use_case.execute(p2)


def test_purchase_domain_invariants():
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    # Invariant: quantity > 0
    with pytest.raises(InvalidPurchaseException):
        Purchase.register(
            id=uuid.uuid4(),
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number="FACT-INV",
            payment_condition="CONTADO",
            issue_date=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            items_payload=[{"product_id": product1, "quantity": 0.0, "unit_cost": 10.0}]
        )

    # Invariant: unit_cost >= 0
    with pytest.raises(InvalidPurchaseException):
        Purchase.register(
            id=uuid.uuid4(),
            company_id=company_id,
            supplier_id=supplier_id,
            invoice_number="FACT-INV",
            payment_condition="CONTADO",
            issue_date=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            items_payload=[{"product_id": product1, "quantity": 5.0, "unit_cost": -1.0}]
        )

    # Invariant: Confirmed purchase cannot be created without items
    with pytest.raises(InvalidPurchaseException):
        Purchase.register(
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


def test_purchase_annulment_state_change():
    repo = InMemoryPurchaseRepository()
    company_id = uuid.uuid4()
    supplier_id = uuid.uuid4()
    product1 = uuid.uuid4()

    supplier_lookup = DummySupplierLookup({supplier_id})
    product_lookup = DummyProductLookup({product1})
    spy_publisher = SpyEventPublisher()

    reg_use_case = RegisterPurchaseUseCase(repo, supplier_lookup, product_lookup, spy_publisher)
    annul_use_case = AnnulPurchaseUseCase(repo, spy_publisher)

    items_payload = [{"product_id": product1, "quantity": 1.0, "unit_cost": 10.0}]
    purchase = Purchase.register(
        id=uuid.uuid4(),
        company_id=company_id,
        supplier_id=supplier_id,
        invoice_number="FACT-ANN",
        payment_condition="CONTADO",
        issue_date=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        items_payload=items_payload
    )
    
    created = reg_use_case.execute(purchase)
    assert created.status == "CONFIRMADA"

    success = annul_use_case.execute(created.id)
    assert success is True
    assert repo.get_by_id(created.id).status == "ANULADA"

    # Verify event published (Confirmed + Annulled)
    assert len(spy_publisher.published_events) == 2
    assert isinstance(spy_publisher.published_events[1], PurchaseAnnulledEvent)
    assert spy_publisher.published_events[1].purchase_id == created.id
