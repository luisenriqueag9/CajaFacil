from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class ArqueoCajaDTO:
    id: UUID
    sesion_id: UUID
    physical_amount: Decimal
    system_amount: Decimal
    difference: Decimal
    supervisor_id: UUID | None
    created_at: datetime
