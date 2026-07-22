from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.brand.domain.entities.brand import Brand

class BrandRepository(ABC):
    
    @abstractmethod
    def create(self, brand: Brand) -> Brand:
        """Persist a new brand in the storage and return it."""
        pass

    @abstractmethod
    def get_by_id(self, brand_id: UUID) -> Brand | None:
        """Retrieve a brand by its unique identifier."""
        pass

    @abstractmethod
    def get_by_name(self, company_id: UUID, name: str) -> Brand | None:
        """
        Retrieve a brand by its name (case-insensitive and whitespace normalized) within a company.
        """
        pass

    @abstractmethod
    def get_all(self, company_id: UUID, status: str | None = None) -> list[Brand]:
        """Retrieve all brands belonging to the company, optionally filtering by status."""
        pass

    @abstractmethod
    def update(self, brand: Brand) -> Brand:
        """Update an existing brand in storage and return it."""
        pass

    @abstractmethod
    def delete(self, brand_id: UUID) -> bool:
        """Delete a brand physically from the storage. Returns True if successful, False otherwise."""
        pass
