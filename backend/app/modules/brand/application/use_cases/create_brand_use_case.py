from app.modules.brand.domain.entities.brand import Brand
from app.modules.brand.domain.repositories.brand_repository import BrandRepository
from app.modules.brand.domain.exceptions.brand_already_exists_exception import BrandAlreadyExistsException
from app.modules.brand.application.utils import clean_brand_name

class CreateBrandUseCase:
    """
    Application use case responsible for creating a new Brand.
    """
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def execute(self, brand: Brand) -> Brand:
        # Normalize the name
        brand.name = clean_brand_name(brand.name)
        brand.validate()

        # Check for uniqueness in the company scope
        existing = self.repository.get_by_name(brand.company_id, brand.name)
        if existing is not None:
            raise BrandAlreadyExistsException(brand.name, brand.company_id)

        return self.repository.create(brand)
