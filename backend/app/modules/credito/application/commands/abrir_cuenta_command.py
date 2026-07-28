from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class AbrirCuentaCreditoCommand:
    company_id: UUID
    client_id: UUID
    credit_limit: Decimal
