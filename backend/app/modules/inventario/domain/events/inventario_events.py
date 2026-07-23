from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class InventarioActualizado:
    product_id: UUID
    company_id: UUID
    quantity_change: Decimal
    new_balance: Decimal
    type: str
    concept: str
    occurred_at: datetime


@dataclass(frozen=True)
class MermaRegistrada:
    merma_id: UUID
    movimiento_id: UUID
    product_id: UUID
    quantity: Decimal
    reason: str
    occurred_at: datetime


@dataclass(frozen=True)
class AjusteInventarioRegistrado:
    ajuste_id: UUID
    movimiento_id: UUID
    product_id: UUID
    physical_quantity: Decimal
    system_quantity: Decimal
    difference: Decimal
    occurred_at: datetime
