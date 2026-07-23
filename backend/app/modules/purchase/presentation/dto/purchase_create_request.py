from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class PurchaseDetailRequest(BaseModel):
    """DTO representing a single item line in the purchase creation payload."""
    product_id: UUID = Field(..., description="UUID of the product being purchased")
    quantity: float = Field(..., gt=0, description="Quantity of the product (must be > 0)")
    unit_cost: float = Field(..., ge=0, description="Unit cost of the product (must be >= 0)")

class PurchaseCreateRequest(BaseModel):
    """DTO representing the payload required to register and confirm a new purchase."""
    company_id: UUID = Field(..., description="UUID of the company context")
    supplier_id: UUID = Field(..., description="UUID of the supplier")
    invoice_number: str = Field(..., min_length=1, max_length=50, description="Invoice number")
    payment_condition: str = Field(..., description="Payment condition (CONTADO or CREDITO)")
    issue_date: datetime = Field(..., description="Invoice emission date")
    items: list[PurchaseDetailRequest] = Field(..., min_length=1, description="List of detail lines")
