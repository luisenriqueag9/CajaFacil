from uuid import UUID
from app.modules.supplier.domain.entities.supplier import Supplier
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.domain.exceptions.supplier_not_found_exception import SupplierNotFoundException

class GetSupplierByIdUseCase:
    """
    Application use case responsible for retrieving a Supplier by its unique identifier.
    """
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: UUID) -> Supplier:
        supplier = self.repository.get_by_id(supplier_id)
        if supplier is None:
            raise SupplierNotFoundException(supplier_id)
        return supplier
