from uuid import UUID
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.domain.exceptions.brand_not_found_exception import BrandNotFoundException

class DeactivateBrandUseCase:
    """
    Application use case responsible for deactivating a Brand.
    """
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def execute(self, brand_id: UUID) -> bool:
        brand = self.repository.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundException(brand_id)

        brand.deactivate()
        self.repository.update(brand)
        return True
