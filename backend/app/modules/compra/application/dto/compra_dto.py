from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List
from app.modules.compra.application.dto.detalle_compra_dto import DetalleCompraDTO

@dataclass(frozen=True)
class CompraDTO:
    id: UUID
    company_id: UUID
    supplier_id: UUID
    invoice_number: str
    payment_condition: str
    issue_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[DetalleCompraDTO]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
