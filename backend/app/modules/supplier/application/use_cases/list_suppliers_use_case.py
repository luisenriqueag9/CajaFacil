from uuid import UUID
from app.modules.supplier.domain.entities.supplier import Supplier
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository

class ListSuppliersUseCase:
    """
    Application use case responsible for listing all suppliers for a company.
    """
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, company_id: UUID, status: str | None = None) -> list[Supplier]:
        return self.repository.get_all(company_id=company_id, status=status)
