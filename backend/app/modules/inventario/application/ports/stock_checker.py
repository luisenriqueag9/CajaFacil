from abc import ABC, abstractmethod
from uuid import UUID
from decimal import Decimal

class StockCheckerPort(ABC):
    """
    Interface definition (Port) allowing Sales (Checkout) to query 
    product stock availability in a fully decoupled manner.
    """
    @abstractmethod
    def has_sufficient_stock(
        self, 
        company_id: UUID, 
        product_id: UUID, 
        quantity: Decimal
    ) -> bool:
        """
        Verifies if there is enough stock available for a checkout transaction,
        taking into account the allows_negative product rules.
        """
        pass
