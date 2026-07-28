from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class CuentaCreditoAbierta:
    credit_id: UUID
    company_id: UUID
    client_id: UUID
    credit_limit: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class LimiteCreditoActualizado:
    credit_id: UUID
    company_id: UUID
    client_id: UUID
    old_limit: Decimal
    new_limit: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class CuentaCreditoInactivada:
    credit_id: UUID
    company_id: UUID
    client_id: UUID
    occurred_at: datetime

@dataclass(frozen=True)
class DeudaRegistrada:
    credit_id: UUID
    company_id: UUID
    client_id: UUID
    amount: Decimal
    reference_id: UUID
    occurred_at: datetime

@dataclass(frozen=True)
class DeudaReversada:
    credit_id: UUID
    company_id: UUID
    client_id: UUID
    amount: Decimal
    reference_id: UUID
    occurred_at: datetime
