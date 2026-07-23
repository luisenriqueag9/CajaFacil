from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.supplier.domain.entities.supplier import Supplier

class SupplierRepository(ABC):
    
    @abstractmethod
    def create(self, supplier: Supplier) -> Supplier:
        """Persist a new supplier in the storage and return it."""
        pass

    @abstractmethod
    def get_by_id(self, supplier_id: UUID) -> Supplier | None:
        """Retrieve a supplier by its unique identifier."""
        pass

    @abstractmethod
    def get_by_tax_id(self, company_id: UUID, tax_id: str) -> Supplier | None:
        """
        Retrieve a supplier by its legal tax identifier (Tax ID/RFC/RTN/NIT) within a company.
        """
        pass

    @abstractmethod
    def get_all(self, company_id: UUID, status: str | None = None) -> list[Supplier]:
        """Retrieve all suppliers belonging to the company, optionally filtering by status."""
        pass

    @abstractmethod
    def update(self, supplier: Supplier) -> Supplier:
        """Update an existing supplier in storage and return it."""
        pass
