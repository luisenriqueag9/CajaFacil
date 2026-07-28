from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List

@dataclass(frozen=True)
class DetalleCompraCommand:
    product_id: UUID
    quantity: Decimal
    unit_cost: Decimal

@dataclass(frozen=True)
class RegistrarCompraCommand:
    company_id: UUID
    supplier_id: UUID
    invoice_number: str
    payment_condition: str
    issue_date: datetime
    items: List[DetalleCompraCommand]
