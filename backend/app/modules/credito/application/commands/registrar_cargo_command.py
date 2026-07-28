from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class RegistrarCargoCreditoCommand:
    company_id: UUID
    client_id: UUID
    amount: Decimal
    reference_id: UUID
