from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.category.domain.entities.category import Category

class CategoryRepository(ABC):
    
    @abstractmethod
    def create(self, category: Category) -> Category:
        """Persist a new category in the storage and return it."""
        pass

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Category | None:
        """Retrieve a category by its unique identifier."""
        pass

    @abstractmethod
    def get_by_name(self, company_id: UUID, name: str) -> Category | None:
        """
        Retrieve a category by its name (case-insensitive and whitespace normalized) within a company.
        """
        pass

    @abstractmethod
    def get_all(self, company_id: UUID, status: str | None = None) -> list[Category]:
        """Retrieve all categories belonging to the company, optionally filtering by status."""
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        """Update an existing category in storage and return it."""
        pass

    @abstractmethod
    def get_default_category(self, company_id: UUID) -> Category | None:
        """Retrieve the default system-protected category for the specified company."""
        pass
