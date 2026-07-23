from uuid import UUID
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.domain.exceptions.supplier_not_found_exception import SupplierNotFoundException

class DeactivateSupplierUseCase:
    """
    Application use case responsible for deactivating a Supplier.
    """
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: UUID) -> bool:
        supplier = self.repository.get_by_id(supplier_id)
        if supplier is None:
            raise SupplierNotFoundException(supplier_id)

        supplier.deactivate()
        self.repository.update(supplier)
        return True
