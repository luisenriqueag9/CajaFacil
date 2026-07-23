from abc import ABC, abstractmethod
from uuid import UUID
from decimal import Decimal

class CreditLookup(ABC):
    @abstractmethod
    def has_active_credit_and_limit(self, company_id: UUID, client_id: UUID, required_amount: Decimal) -> bool:
        """Verify that a client has an active credit line and sufficient limit."""
        pass
