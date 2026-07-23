from abc import ABC, abstractmethod
from uuid import UUID
from typing import NamedTuple

class ProductDetails(NamedTuple):
    exists: bool
    active: bool
    controls_stock: bool
    allows_negative: bool


class ProductLookup(ABC):
    @abstractmethod
    def get_details(self, company_id: UUID, product_id: UUID) -> ProductDetails:
        """
        Retrieves logical stock-control and existence parameters for a product.
        """
        pass
