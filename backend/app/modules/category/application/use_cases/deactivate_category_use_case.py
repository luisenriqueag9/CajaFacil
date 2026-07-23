from uuid import UUID
from app.modules.category.domain.repositories.category_repository import CategoryRepository
from app.modules.category.domain.exceptions.category_not_found_exception import CategoryNotFoundException

class DeactivateCategoryUseCase:
    """
    Application use case responsible for deactivating a Category.
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, category_id: UUID) -> bool:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException(category_id)

        category.deactivate()
        self.repository.update(category)
        return True
