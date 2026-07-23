from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class RegistrarMovimientoRequest(BaseModel):
    product_id: UUID = Field(..., description="UUID of the product affected")
    type: str = Field(..., description="ENTRADA, SALIDA")
    concept: str = Field(..., description="COMPRA, VENTA, ANULACION_VENTA, DEVOLUCION_PROVEEDOR, INVENTARIO_INICIAL")
    quantity: Decimal = Field(..., description="Quantity of items")
    created_by: UUID = Field(..., description="UUID of the user recording the movement")
    origin_document_id: UUID | None = Field(None, description="Optional original document identifier")
    notes: str | None = Field(None, max_length=300, description="Optional audit notes")


class RegistrarMermaRequest(BaseModel):
    product_id: UUID = Field(..., description="UUID of the product affected")
    quantity: Decimal = Field(..., description="Quantity wasted")
    reason: str = Field(..., description="ROTURA, VENCIMIENTO, ROBO, OTRO")
    created_by: UUID = Field(..., description="UUID of the user recording the waste")
    description: str | None = Field(None, max_length=200, description="Optional description details")


class RegistrarAjusteRequest(BaseModel):
    product_id: UUID = Field(..., description="UUID of the product affected")
    physical_quantity: Decimal = Field(..., description="Actual quantity counted physically in inventory count")
    supervisor_id: UUID = Field(..., description="UUID of the supervisor authorizing the adjustment")
    notes: str | None = Field(None, max_length=300, description="Optional reason for the adjustment discrepancy")
