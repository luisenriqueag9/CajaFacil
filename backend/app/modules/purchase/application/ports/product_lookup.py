from abc import ABC, abstractmethod
from uuid import UUID

class ProductLookup(ABC):
    @abstractmethod
    def exists_and_active(self, company_id: UUID, product_id: UUID) -> bool:
        """Verify that a product exists and is active under the company."""
        pass
