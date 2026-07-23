from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class PurchaseDetailResponse(BaseModel):
    """DTO representing a single item line in the purchase response payload."""
    id: UUID
    purchase_id: UUID
    product_id: UUID
    quantity: float
    unit_cost: float
    line_total: float

    model_config = {
        "from_attributes": True
    }

class PurchaseResponse(BaseModel):
    """DTO representing the data payload returned containing purchase details."""
    id: UUID
    company_id: UUID
    supplier_id: UUID
    invoice_number: str
    payment_condition: str
    issue_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    subtotal: float
    tax: float
    total: float
    items: list[PurchaseDetailResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }
