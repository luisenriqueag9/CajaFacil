from uuid import UUID
from app.modules.purchase.domain.entities.purchase import Purchase
from app.modules.purchase.domain.repositories.purchase_repository import PurchaseRepository

class ListPurchasesUseCase:
    """
    Application use case to retrieve a list of purchases, optionally filtering by status and supplier.
    """
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository

    def execute(
        self, 
        company_id: UUID, 
        status: str | None = None, 
        supplier_id: UUID | None = None
    ) -> list[Purchase]:
        return self.repository.get_all(company_id=company_id, status=status, supplier_id=supplier_id)
