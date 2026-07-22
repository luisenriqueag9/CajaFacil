from uuid import UUID
from app.modules.brand.domain.entities.brand import Brand
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.domain.exceptions.brand_not_found_exception import BrandNotFoundException
from app.modules.brand.domain.exceptions.brand_already_exists_exception import BrandAlreadyExistsException
from app.common.exceptions import ValidationException
from app.modules.brand.application.utils import clean_brand_name

class UpdateBrandUseCase:
    """
    Application use case responsible for updating an existing Brand.
    """
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def execute(self, brand_id: UUID, updates: dict[str, object]) -> Brand:
        if not updates:
            raise ValidationException("No se enviaron campos para actualizar.")

        brand = self.repository.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundException(brand_id)

        # If name is updated, clean/normalize it first and check for uniqueness
        if "name" in updates and updates["name"] is not None:
            cleaned_name = clean_brand_name(str(updates["name"]))
            if cleaned_name != brand.name:
                existing = self.repository.get_by_name(brand.company_id, cleaned_name)
                if existing is not None and existing.id != brand.id:
                    raise BrandAlreadyExistsException(cleaned_name, brand.company_id)
                updates["name"] = cleaned_name

        # Apply updates using domain behaviors
        if "name" in updates:
            brand.rename(str(updates["name"]))
            
        if "status" in updates:
            new_status = str(updates["status"])
            if new_status == "ACTIVO":
                brand.activate()
            elif new_status == "INACTIVO":
                brand.deactivate()
            else:
                brand.status = new_status
                brand.validate()

        return self.repository.update(brand)
