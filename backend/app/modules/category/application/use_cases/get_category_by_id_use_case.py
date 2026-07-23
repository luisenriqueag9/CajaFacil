from uuid import UUID
from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.repositories.category_repository import CategoryRepository
from app.modules.category.domain.exceptions.category_not_found_exception import CategoryNotFoundException

class GetCategoryByIdUseCase:
    """
    Application use case responsible for retrieving a Category by its unique identifier.
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, category_id: UUID) -> Category:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException(category_id)
        return category
