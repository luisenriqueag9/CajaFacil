from app.modules.supplier.domain.entities.supplier import Supplier
from app.modules.supplier.domain.repositories.supplier_repository import SupplierRepository
from app.modules.supplier.domain.exceptions.supplier_already_exists_exception import SupplierAlreadyExistsException
from app.modules.supplier.application.utils import clean_supplier_name, clean_tax_id

class CreateSupplierUseCase:
    """
    Application use case responsible for registering a new Supplier.
    """
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def execute(self, supplier: Supplier) -> Supplier:
        # Normalize the name and tax_id
        supplier.name = clean_supplier_name(supplier.name)
        supplier.tax_id = clean_tax_id(supplier.tax_id)
        supplier.validate()

        # Check for tax ID uniqueness in the company scope if tax_id is provided
        if supplier.tax_id is not None:
            existing = self.repository.get_by_tax_id(supplier.company_id, supplier.tax_id)
            if existing is not None:
                raise SupplierAlreadyExistsException(supplier.tax_id, supplier.company_id)

        return self.repository.create(supplier)
