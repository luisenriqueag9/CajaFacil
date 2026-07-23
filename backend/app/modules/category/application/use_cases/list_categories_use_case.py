from uuid import UUID
from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.repositories.category_repository import CategoryRepository

class ListCategoriesUseCase:
    """
    Application use case responsible for listing all categories for a company.
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, company_id: UUID, status: str | None = None) -> list[Category]:
        return self.repository.get_all(company_id=company_id, status=status)
