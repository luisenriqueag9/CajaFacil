from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class PurchaseConfirmedEvent:
    purchase_id: UUID
    company_id: UUID
    supplier_id: UUID
    total: float
    payment_condition: str
    items: list[dict]  # list of {"product_id": UUID, "quantity": float, "unit_cost": float}
    occurred_at: datetime

@dataclass
class PurchaseAnnulledEvent:
    purchase_id: UUID
    company_id: UUID
    supplier_id: UUID
    occurred_at: datetime
