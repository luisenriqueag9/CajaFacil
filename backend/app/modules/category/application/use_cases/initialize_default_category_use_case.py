import uuid
from datetime import datetime, timezone
from uuid import UUID
from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.repositories.category_repository import CategoryRepository

class InitializeDefaultCategoryUseCase:
    """
    Application use case responsible for creating the system-protected default category ('Sin Clasificar').
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, company_id: UUID) -> Category:
        # Check if a default category already exists for this company
        existing = self.repository.get_default_category(company_id)
        if existing is not None:
            return existing

        category_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        # Uses the initialize_default static factory to enforce Domain invariants
        default_category = Category.initialize_default(
            id=category_id,
            company_id=company_id,
            name="Sin Clasificar",
            created_at=now,
            updated_at=now
        )

        return self.repository.create(default_category)
