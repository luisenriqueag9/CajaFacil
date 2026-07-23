from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.repositories.category_repository import CategoryRepository
from app.modules.category.domain.exceptions.category_already_exists_exception import CategoryAlreadyExistsException
from app.modules.category.application.utils import clean_category_name

class CreateCategoryUseCase:
    """
    Application use case responsible for registering a new Category.
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, category: Category) -> Category:
        # Normalize the name
        category.name = clean_category_name(category.name)
        category.validate()

        # Check for uniqueness in the company scope
        existing = self.repository.get_by_name(category.company_id, category.name)
        if existing is not None:
            raise CategoryAlreadyExistsException(category.name, category.company_id)

        return self.repository.create(category)
