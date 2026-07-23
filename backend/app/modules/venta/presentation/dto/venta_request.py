from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class DetalleVentaRequest(BaseModel):
    product_id: UUID = Field(..., description="UUID of the product")
    quantity: Decimal = Field(..., description="Quantity sold")
    unit_price: Decimal = Field(..., description="Price per unit pactado")
    discount: Decimal = Field(Decimal("0.00"), description="Discount on the line")
    tax_rate: Decimal = Field(Decimal("0.15"), description="Tax rate applied, e.g. 0.15")
    tax_amount: Decimal = Field(..., description="Total tax amount for the line")
    subtotal: Decimal = Field(..., description="Subtotal of the line")
    total: Decimal = Field(..., description="Total of the line")


class FormaPagoAceptadaRequest(BaseModel):
    payment_method: str = Field(..., description="EFECTIVO, TARJETA, CREDITO")
    amount: Decimal = Field(..., description="Amount paid using this method")
    transaction_reference: str | None = Field(None, max_length=100, description="Optional bank or credit reference")


class ConfirmarVentaRequest(BaseModel):
    company_id: UUID = Field(..., description="Tenant company UUID")
    box_id: UUID = Field(..., description="Box session UUID")
    user_id: UUID = Field(..., description="Cajero user UUID")
    client_id: UUID | None = Field(None, description="Client UUID; required if payment method is CREDITO")
    invoice_number: str | None = Field(None, max_length=50, description="Optional invoice sequence number")
    
    subtotal: Decimal = Field(..., description="Venta subtotal")
    discount: Decimal = Field(Decimal("0.00"), description="Venta total discount")
    tax: Decimal = Field(..., description="Venta total tax")
    total: Decimal = Field(..., description="Venta total commercial value")
    
    details: list[DetalleVentaRequest] = Field(..., description="List of items sold")
    payments: list[FormaPagoAceptadaRequest] = Field(..., description="List of payment methods")
