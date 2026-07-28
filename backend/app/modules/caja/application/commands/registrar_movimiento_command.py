from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class RegistrarMovimientoCommand:
    sesion_id: UUID
    type: str  # INGRESO, EGRESO
    amount: Decimal
    payment_method: str  # EFECTIVO, TARJETA, TRANSFERENCIA, CREDITO
    concept: str
    origin_context: str | None = None
    origin_document_id: UUID | None = None
