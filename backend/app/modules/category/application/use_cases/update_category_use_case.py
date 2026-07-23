from uuid import UUID
from app.modules.category.domain.entities.category import Category
from app.modules.category.domain.repositories.category_repository import CategoryRepository
from app.modules.category.domain.exceptions.category_not_found_exception import CategoryNotFoundException
from app.modules.category.domain.exceptions.category_already_exists_exception import CategoryAlreadyExistsException
from app.common.exceptions import ValidationException
from app.modules.category.application.utils import clean_category_name

class UpdateCategoryUseCase:
    """
    Application use case responsible for updating/renaming an existing Category.
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, category_id: UUID, updates: dict[str, object]) -> Category:
        if not updates:
            raise ValidationException("No se enviaron campos para actualizar.")

        category = self.repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundException(category_id)

        # If name is updated, clean/normalize it first and check for uniqueness
        if "name" in updates and updates["name"] is not None:
            cleaned_name = clean_category_name(str(updates["name"]))
            if cleaned_name != category.name:
                existing = self.repository.get_by_name(category.company_id, cleaned_name)
                if existing is not None and existing.id != category.id:
                    raise CategoryAlreadyExistsException(cleaned_name, category.company_id)
                updates["name"] = cleaned_name

        # Apply updates using domain behaviors
        if "name" in updates:
            category.rename(str(updates["name"]))
            
        if "status" in updates:
            new_status = str(updates["status"])
            if new_status == "ACTIVO":
                category.activate()
            elif new_status == "INACTIVO":
                category.deactivate()
            else:
                category.status = new_status
                category.validate()

        return self.repository.update(category)
