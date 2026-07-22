from uuid import UUID
from app.modules.product.domain.repositories.product_repository import ProductRepository
from app.modules.product.domain.exceptions.product_not_found_exception import ProductNotFoundException

class DeactivateProductUseCase:
    """
    Application use case responsible for deactivating an existing Product (soft-delete).
    """
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: UUID) -> bool:
        # Verify product exists first to raise domain exception if not
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundException(product_id)

        return self.repository.deactivate(product_id)
