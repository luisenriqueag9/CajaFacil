from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class UpdateProductRequest(BaseModel):
    """DTO representing the partial payload required to update an existing Product."""
    internal_code: str | None = Field(None, max_length=50, description="Unique internal code")
    barcode: str | None = Field(None, max_length=50, description="Barcode")
    name: str | None = Field(None, max_length=100, description="Name")
    description: str | None = Field(None, description="Detailed description")
    category_id: UUID | None = Field(None, description="Category ID")
    brand_id: UUID | None = Field(None, description="Brand ID")
    unit_id: UUID | None = Field(None, description="Unit ID")
    cost: Decimal | None = Field(None, ge=0, description="Cost (must be non-negative)")
    price: Decimal | None = Field(None, ge=0, description="Sale price (must be non-negative)")
    tax_rate: Decimal | None = Field(None, ge=0, description="Tax rate percentage (must be non-negative)")
    controls_stock: bool | None = Field(None, description="Track inventory flag")
    allows_decimal: bool | None = Field(None, description="Allows decimal quantity flag")
    is_perishable: bool | None = Field(None, description="Perishable flag")
    minimum_stock: Decimal | None = Field(None, ge=0, description="Minimum stock limit")
    status: str | None = Field(None, description="Status (ACTIVO/INACTIVO)")
