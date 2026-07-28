from datetime import datetime
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field

class DetalleCompraRequest(BaseModel):
    """DTO que representa una linea de item en la creacion de la compra."""
    product_id: UUID = Field(..., description="UUID del producto adquirido")
    quantity: Decimal = Field(..., gt=Decimal("0.0000"), description="Cantidad del producto (debe ser > 0)")
    unit_cost: Decimal = Field(..., ge=Decimal("0.0000"), description="Costo unitario del producto (debe ser >= 0)")

class RegistrarCompraRequest(BaseModel):
    """DTO que representa la solicitud para registrar una compra."""
    company_id: UUID = Field(..., description="UUID de la empresa")
    supplier_id: UUID = Field(..., description="UUID del proveedor")
    invoice_number: str = Field(..., min_length=1, max_length=50, description="Numero de factura")
    payment_condition: str = Field(..., description="Condicion de pago (CONTADO o CREDITO)")
    issue_date: datetime = Field(..., description="Fecha de emision de la factura")
    items: list[DetalleCompraRequest] = Field(..., min_length=1, description="Lista de lineas de detalle")
