from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class VentaConfirmada:
    venta_id: UUID
    company_id: UUID
    box_id: UUID
    user_id: UUID
    client_id: UUID | None
    invoice_number: str | None
    total: Decimal
    items: list[dict]  # List of {"product_id": UUID, "quantity": Decimal, "unit_price": Decimal}
    cash_amount: Decimal
    credit_amount: Decimal
    occurred_at: datetime

@dataclass(frozen=True)
class VentaAnulada:
    venta_id: UUID
    company_id: UUID
    box_id: UUID
    client_id: UUID | None
    total: Decimal
    items: list[dict]  # List of {"product_id": UUID, "quantity": Decimal}
    cash_amount: Decimal
    credit_amount: Decimal
    voided_by: UUID
    void_reason: str
    occurred_at: datetime
