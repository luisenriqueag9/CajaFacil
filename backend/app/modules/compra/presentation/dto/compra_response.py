from datetime import datetime
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field

class DetalleCompraResponse(BaseModel):
    """DTO que representa una linea de item en la respuesta de la compra."""
    id: UUID
    purchase_id: UUID
    product_id: UUID
    quantity: Decimal
    unit_cost: Decimal
    line_total: Decimal

    model_config = {
        "from_attributes": True
    }

class CompraResponse(BaseModel):
    """DTO que representa los detalles retornados de una compra."""
    id: UUID
    company_id: UUID
    supplier_id: UUID
    invoice_number: str
    payment_condition: str
    issue_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    items: list[DetalleCompraResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }
