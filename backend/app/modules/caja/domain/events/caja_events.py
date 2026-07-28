from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class SesionCajaAbierta:
    sesion_id: UUID
    caja_id: UUID
    company_id: UUID
    user_id: UUID
    opening_balance: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class MovimientoCajaRegistrado:
    movimiento_id: UUID
    sesion_id: UUID
    type: str
    amount: Decimal
    payment_method: str
    concept: str
    occurred_at: datetime

@dataclass(frozen=True)
class ArqueoCajaRealizado:
    sesion_id: UUID
    physical_amount: Decimal
    system_amount: Decimal
    difference: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class SesionCajaCerrada:
    sesion_id: UUID
    caja_id: UUID
    closed_at: datetime
    occurred_at: datetime

@dataclass(frozen=True)
class MovimientoCajaAnulado:
    movimiento_id: UUID
    sesion_id: UUID
    concept: str
    amount: Decimal
    occurred_at: datetime
