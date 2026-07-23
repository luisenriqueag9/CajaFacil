from datetime import datetime, timezone
from uuid import UUID
from app.modules.purchase.domain.repositories.purchase_repository import PurchaseRepository
from app.modules.purchase.domain.exceptions.purchase_not_found_exception import PurchaseNotFoundException
from app.modules.purchase.application.ports.event_publisher import EventPublisher
from app.modules.purchase.application.events.purchase_events import PurchaseAnnulledEvent

class AnnulPurchaseUseCase:
    """
    Application use case to annul an already confirmed purchase.
    """
    def __init__(self, repository: PurchaseRepository, event_publisher: EventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, purchase_id: UUID) -> bool:
        purchase = self.repository.get_by_id(purchase_id)
        if purchase is None:
            raise PurchaseNotFoundException(purchase_id)

        purchase.annul()
        self.repository.update(purchase)

        # Publish Event
        event = PurchaseAnnulledEvent(
            purchase_id=purchase.id,
            company_id=purchase.company_id,
            supplier_id=purchase.supplier_id,
            occurred_at=datetime.now(timezone.utc)
        )
        self.event_publisher.publish(event)

        return True
