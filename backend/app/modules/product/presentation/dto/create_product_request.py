from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class CreateProductRequest(BaseModel):
    """DTO representing the payload required to create a new Product."""
    company_id: UUID = Field(..., description="ID of the company (tenant) that owns this product")
    internal_code: str = Field(..., max_length=50, description="Unique internal code for the product in the company scope")
    barcode: str | None = Field(None, max_length=50, description="Optional barcode")
    name: str = Field(..., max_length=100, description="Name of the product")
    description: str | None = Field(None, description="Detailed description")
    category_id: UUID = Field(..., description="ID of the category")
    brand_id: UUID = Field(..., description="ID of the brand")
    unit_id: UUID = Field(..., description="ID of the unit of measure")
    cost: Decimal = Field(..., ge=0, description="Product cost (must be non-negative)")
    price: Decimal = Field(..., ge=0, description="Product sale price (must be non-negative)")
    tax_rate: Decimal = Field(..., ge=0, description="Product tax rate percentage (must be non-negative)")
    controls_stock: bool = Field(True, description="Flag indicating if inventory is tracked")
    allows_decimal: bool = Field(False, description="Flag indicating if fractional quantity is allowed")
    is_perishable: bool = Field(False, description="Flag indicating if the product has an expiration date")
    minimum_stock: Decimal = Field(Decimal("0.00"), ge=0, description="Minimum stock alert limit")
    status: str = Field("ACTIVO", description="Status of the product (ACTIVO/INACTIVO)")
