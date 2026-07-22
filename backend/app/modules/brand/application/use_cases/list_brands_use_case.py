from uuid import UUID
from app.modules.brand.domain.entities.brand import Brand
from app.modules.brand.domain.repositories.brand_repository import BrandRepository

class ListBrandsUseCase:
    """
    Application use case responsible for retrieving all brands for a company.
    """
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def execute(self, company_id: UUID, status: str | None = None) -> list[Brand]:
        return self.repository.get_all(company_id=company_id, status=status)
