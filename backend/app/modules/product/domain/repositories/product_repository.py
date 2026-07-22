from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.product.domain.entities.product import Product

class ProductRepository(ABC):
    """
    Interface for Product domain repository operations.
    Follows DDD and Clean Architecture guidelines.
    """

    @abstractmethod
    def create(self, product: Product) -> Product:
        """
        Persist a new product in the storage and return it.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product | None:
        """
        Retrieve a product by its unique identifier.
        """
        pass

    @abstractmethod
    def get_by_internal_code(self, company_id: UUID, internal_code: str) -> Product | None:
        """
        Retrieve a product by its internal code within a specific company.
        """
        pass

    @abstractmethod
    def get_by_barcode(self, company_id: UUID, barcode: str) -> Product | None:
        """
        Retrieve a product by its barcode within a specific company.
        """
        pass

    @abstractmethod
    def get_all(
        self,
        company_id: UUID,
        category_id: UUID | None = None,
        brand_id: UUID | None = None,
        status: str | None = None,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[Product]:
        """
        Retrieve all products matching the query parameters within a specific company.
        Supports pagination, status filtering, category/brand filter, and name/barcode search.
        """
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        """
        Update an existing product in the storage and return it.
        """
        pass
