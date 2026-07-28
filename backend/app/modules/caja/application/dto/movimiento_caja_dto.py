from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class MovimientoCajaDTO:
    id: UUID
    sesion_id: UUID
    type: str
    amount: Decimal
    payment_method: str
    concept: str
    origin_context: str | None
    origin_document_id: UUID | None
    voided: bool
    created_at: datetime
