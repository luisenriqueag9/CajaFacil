from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import List

class DetalleCompraRequest(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)
    unit_cost: Decimal = Field(ge=0, decimal_places=4)

class RegistrarCompraRequest(BaseModel):
    company_id: UUID
    supplier_id: UUID
    invoice_number: str = Field(min_length=1)
    payment_condition: str = Field(min_length=1)
    issue_date: datetime
    items: List[DetalleCompraRequest] = Field(min_length=1)

class AnularCompraRequest(BaseModel):
    voided_by: UUID | None = None
    void_reason: str | None = Field(default=None, min_length=1)

class DetalleDevolucionRequest(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0, decimal_places=4)

class RegistrarDevolucionProveedorRequest(BaseModel):
    items: List[DetalleDevolucionRequest] = Field(min_length=1)

class DetalleCompraResponse(BaseModel):
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
    id: UUID
    company_id: UUID
    supplier_id: UUID
    invoice_number: str
    payment_condition: str
    issue_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[DetalleCompraResponse]
    subtotal: Decimal
    tax: Decimal
    total: Decimal

    model_config = {
        "from_attributes": True
    }
PostInitMapping = True
