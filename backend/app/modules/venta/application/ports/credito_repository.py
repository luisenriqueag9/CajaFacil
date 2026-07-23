from abc import ABC, abstractmethod
from uuid import UUID
from decimal import Decimal

class CreditoRepository(ABC):
    @abstractmethod
    def registrar_deuda(
        self,
        company_id: UUID,
        client_id: UUID,
        amount: Decimal,
        reference_id: UUID
    ) -> None:
        """Registers a new credit balance/debt for a client inside the shared transaction."""
        pass

    @abstractmethod
    def reversar_deuda(
        self,
        company_id: UUID,
        client_id: UUID,
        amount: Decimal,
        reference_id: UUID
    ) -> None:
        """Reverses a previously registered debt inside the shared transaction."""
        pass
