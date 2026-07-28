from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class DetalleCompraDTO:
    id: UUID
    purchase_id: UUID
    product_id: UUID
    quantity: Decimal
    unit_cost: Decimal
    line_total: Decimal
