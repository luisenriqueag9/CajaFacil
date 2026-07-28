from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class CreditoDTO:
    id: UUID
    company_id: UUID
    client_id: UUID
    credit_limit: Decimal
    balance: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
