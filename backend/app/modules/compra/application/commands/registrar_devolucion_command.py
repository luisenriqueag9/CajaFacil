from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from typing import List

@dataclass(frozen=True)
class DetalleDevolucionCommand:
    product_id: UUID
    quantity: Decimal

@dataclass(frozen=True)
class RegistrarDevolucionProveedorCommand:
    purchase_id: UUID
    items: List[DetalleDevolucionCommand]
