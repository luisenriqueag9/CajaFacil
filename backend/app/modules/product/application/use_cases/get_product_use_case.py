from uuid import UUID
from app.modules.product.domain.entities.product import Product
from app.modules.product.domain.repositories.product_repository import ProductRepository
from app.modules.product.domain.exceptions.product_not_found_exception import ProductNotFoundException

class GetProductUseCase:
    """
    Application use case responsible for retrieving a single Product by its ID.
    """
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: UUID) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundException(product_id)
        return product
