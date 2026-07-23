from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class DetalleVentaResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    discount: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    subtotal: Decimal
    total: Decimal

    model_config = {
        "from_attributes": True
    }


class FormaPagoAceptadaResponse(BaseModel):
    payment_method: str
    amount: Decimal
    transaction_reference: str | None

    model_config = {
        "from_attributes": True
    }


class VentaResponse(BaseModel):
    id: UUID
    company_id: UUID
    box_id: UUID
    user_id: UUID
    client_id: UUID | None
    invoice_number: str | None
    
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal
    status: str
    
    created_at: datetime
    updated_at: datetime
    
    details: list[DetalleVentaResponse]
    payments: list[FormaPagoAceptadaResponse]

    voided_by: UUID | None
    voided_at: datetime | None
    void_reason: str | None

    model_config = {
        "from_attributes": True
    }
