from datetime import datetime, timezone
from uuid import UUID
from app.modules.purchase.domain.entities.purchase import Purchase
from app.modules.purchase.domain.repositories.purchase_repository import PurchaseRepository
from app.modules.purchase.domain.exceptions.purchase_already_exists_exception import PurchaseAlreadyExistsException
from app.modules.purchase.domain.exceptions.invalid_purchase_exception import InvalidPurchaseException
from app.modules.purchase.application.ports.supplier_lookup import SupplierLookup
from app.modules.purchase.application.ports.product_lookup import ProductLookup
from app.modules.purchase.application.ports.event_publisher import EventPublisher
from app.modules.purchase.application.events.purchase_events import PurchaseConfirmedEvent

class RegisterPurchaseUseCase:
    """
    Application use case to register and confirm a purchase directly.
    """
    def __init__(
        self, 
        repository: PurchaseRepository, 
        supplier_lookup: SupplierLookup,
        product_lookup: ProductLookup,
        event_publisher: EventPublisher
    ):
        self.repository = repository
        self.supplier_lookup = supplier_lookup
        self.product_lookup = product_lookup
        self.event_publisher = event_publisher

    def execute(self, purchase: Purchase) -> Purchase:
        # 1. Verify that the supplier exists and is active
        if not self.supplier_lookup.exists_and_active(purchase.company_id, purchase.supplier_id):
            raise InvalidPurchaseException(
                f"El proveedor '{purchase.supplier_id}' no existe o está inactivo."
            )

        # 2. Verify that each product exists and is active
        for item in purchase.items:
            if not self.product_lookup.exists_and_active(purchase.company_id, item.product_id):
                raise InvalidPurchaseException(
                    f"El producto '{item.product_id}' no existe o está inactivo."
                )

        # 3. Check duplicate invoice number for the supplier within the company
        existing = self.repository.get_by_invoice_number(
            purchase.company_id, 
            purchase.supplier_id, 
            purchase.invoice_number
        )
        if existing is not None:
            raise PurchaseAlreadyExistsException(purchase.invoice_number, purchase.supplier_id)

        # 4. Persist
        created_purchase = self.repository.create(purchase)

        # 5. Publish Event
        items_payload = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_cost": item.unit_cost
            }
            for item in created_purchase.items
        ]
        
        event = PurchaseConfirmedEvent(
            purchase_id=created_purchase.id,
            company_id=created_purchase.company_id,
            supplier_id=created_purchase.supplier_id,
            total=created_purchase.total,
            payment_condition=created_purchase.payment_condition,
            items=items_payload,
            occurred_at=datetime.now(timezone.utc)
        )
        self.event_publisher.publish(event)

        return created_purchase
