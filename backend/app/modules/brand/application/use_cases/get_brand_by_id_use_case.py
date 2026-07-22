from uuid import UUID
from app.modules.brand.domain.entities.brand import Brand
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.domain.exceptions.brand_not_found_exception import BrandNotFoundException

class GetBrandByIdUseCase:
    """
    Application use case responsible for retrieving a Brand by its unique identifier.
    """
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def execute(self, brand_id: UUID) -> Brand:
        brand = self.repository.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundException(brand_id)
        return brand
