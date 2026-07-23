from abc import ABC, abstractmethod
from uuid import UUID
from decimal import Decimal

class MovimientoInventarioRepository(ABC):
    @abstractmethod
    def registrar_movimiento(
        self,
        company_id: UUID,
        product_id: UUID,
        quantity: Decimal,
        tipo: str,  # SALIDA, ENTRADA
        concept: str,  # VENTA, ANULACION_VENTA
        reference_id: UUID
    ) -> None:
        """Registers a movement of stock for a product inside the shared transaction."""
        pass
