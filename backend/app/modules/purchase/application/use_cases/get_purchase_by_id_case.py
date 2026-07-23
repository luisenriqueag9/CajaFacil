from uuid import UUID
from app.modules.purchase.domain.entities.purchase import Purchase
from app.modules.purchase.domain.repositories.purchase_repository import PurchaseRepository
from app.modules.purchase.domain.exceptions.purchase_not_found_exception import PurchaseNotFoundException

class GetPurchaseByIdUseCase:
    """
    Application use case to retrieve a single purchase by its unique identifier.
    """
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository

    def execute(self, purchase_id: UUID) -> Purchase:
        purchase = self.repository.get_by_id(purchase_id)
        if purchase is None:
            raise PurchaseNotFoundException(purchase_id)
        return purchase
