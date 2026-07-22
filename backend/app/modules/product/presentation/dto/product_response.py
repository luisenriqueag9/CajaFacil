from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ProductResponse(BaseModel):
    """DTO representing the product data returned to the client."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    internal_code: str
    barcode: str | None
    name: str
    description: str | None
    category_id: UUID
    brand_id: UUID
    unit_id: UUID
    cost: Decimal
    price: Decimal
    tax_rate: Decimal
    controls_stock: bool
    allows_decimal: bool
    is_perishable: bool
    minimum_stock: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
