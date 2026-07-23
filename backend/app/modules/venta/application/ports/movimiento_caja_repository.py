from abc import ABC, abstractmethod
from uuid import UUID
from decimal import Decimal

class MovimientoCajaRepository(ABC):
    @abstractmethod
    def registrar_movimiento(
        self,
        company_id: UUID,
        box_id: UUID,
        user_id: UUID,
        amount: Decimal,
        tipo: str,  # INGRESO, EGRESO
        concept: str,  # VENTA, ANULACION_VENTA
        reference_id: UUID
    ) -> None:
        """Registers a cash flow movement inside the shared transaction."""
        pass
