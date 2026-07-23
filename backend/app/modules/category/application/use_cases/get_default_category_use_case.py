from uuid import UUID
from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.repositories.category_repository import CategoryRepository

class GetDefaultCategoryUseCase:
    """
    Application use case responsible for retrieving the system-protected default category ('Sin Clasificar').
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, company_id: UUID) -> Category:
        category = self.repository.get_default_category(company_id)
        if category is None:
            # Resiliency: If it hasn't been initialized yet, initialize it on-demand
            from app.modules.category.application.use_cases.initialize_default_category_use_case import InitializeDefaultCategoryUseCase
            init_use_case = InitializeDefaultCategoryUseCase(self.repository)
            return init_use_case.execute(company_id)
        return category
