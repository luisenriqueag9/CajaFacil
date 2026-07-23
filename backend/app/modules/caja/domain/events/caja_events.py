from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class CajaAbierta:
    caja_id: UUID
    company_id: UUID
    user_id: UUID
    opening_balance: Decimal
    occurred_at: datetime


@dataclass(frozen=True)
class MovimientoCajaRegistrado:
    movimiento_id: UUID
    caja_id: UUID
    company_id: UUID
    amount: Decimal
    type: str
    concept: str
    occurred_at: datetime


@dataclass(frozen=True)
class ArqueoRealizado:
    arqueo_id: UUID
    caja_id: UUID
    company_id: UUID
    physical_amount: Decimal
    difference: Decimal
    occurred_at: datetime


@dataclass(frozen=True)
class CajaCerrada:
    caja_id: UUID
    company_id: UUID
    physical_amount: Decimal
    system_amount: Decimal
    difference: Decimal
    occurred_at: datetime
