from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class AbrirSesionCommand:
    caja_id: UUID
    company_id: UUID
    user_id: UUID
    opening_balance: Decimal
