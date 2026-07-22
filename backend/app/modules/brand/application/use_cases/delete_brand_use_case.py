from uuid import UUID
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.domain.exceptions.brand_not_found_exception import BrandNotFoundException

class DeleteBrandUseCase:
    """
    Application use case responsible for physically deleting a Brand.
    """
    def __init__(self, repository: BrandRepository, check_association_service=None):
        self.repository = repository
        self.check_association_service = check_association_service

    def execute(self, brand_id: UUID) -> bool:
        brand = self.repository.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundException(brand_id)

        # Integration point prepared to check for associated products
        # without coupling directly to the Product repository/module
        if self.check_association_service is not None:
            if self.check_association_service.has_products(brand_id):
                from app.common.exceptions import ValidationException
                raise ValidationException("No se puede eliminar la marca porque tiene productos asociados.")

        return self.repository.delete(brand_id)
