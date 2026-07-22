from uuid import UUID
from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.repositories.product_repository import ProductRepository

class ListProductsUseCase:
    """
    Application use case responsible for retrieving all products for a specific company with pagination and filters.
    """
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(
        self,
        company_id: UUID,
        category_id: UUID | None = None,
        brand_id: UUID | None = None,
        status: str | None = None,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[Product]:
        return self.repository.get_all(
            company_id=company_id,
            category_id=category_id,
            brand_id=brand_id,
            status=status,
            search=search,
            limit=limit,
            offset=offset
        )
