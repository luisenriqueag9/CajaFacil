from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.company.domain.entities.company import Company

class CompanyRepository(ABC):
    
    @abstractmethod
    def create(self, company: Company) -> Company:
        """Persist a new company in the storage and return it."""
        pass

    @abstractmethod
    def get_by_tax_id(self, tax_id: str) -> Company | None:
        """
        Retrieve a company by its tax identifier (RTN).
        Returns None if no company exists.
        """
        pass
        
    @abstractmethod
    def get_by_id(self, company_id: UUID) -> Company | None:
        """Retrieve a company by its unique identifier."""
        pass
        
    @abstractmethod
    def get_all(self) -> list[Company]:
        """Retrieve all registered companies."""
        pass
        
    @abstractmethod
    def update(self, company: Company) -> Company:
        """Update an existing company in the storage and return it."""
        pass

