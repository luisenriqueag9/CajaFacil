from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class ActualizarLimiteCreditoCommand:
    credit_id: UUID
    new_limit: Decimal
