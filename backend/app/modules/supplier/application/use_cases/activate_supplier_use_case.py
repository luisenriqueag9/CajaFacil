from uuid import UUID
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.domain.exceptions.supplier_not_found_exception import SupplierNotFoundException

class ActivateSupplierUseCase:
    """
    Application use case responsible for activating a Supplier.
    """
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier_id: UUID) -> bool:
        supplier = self.repository.get_by_id(supplier_id)
        if supplier is None:
            raise SupplierNotFoundException(supplier_id)

        supplier.activate()
        self.repository.update(supplier)
        return True
