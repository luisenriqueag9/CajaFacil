from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class MermaResponse(BaseModel):
    id: UUID
    reason: str
    description: str | None

    model_config = {
        "from_attributes": True
    }


class AjusteInventarioResponse(BaseModel):
    id: UUID
    physical_quantity: Decimal
    system_quantity: Decimal
    difference: Decimal

    model_config = {
        "from_attributes": True
    }


class MovimientoInventarioResponse(BaseModel):
    id: UUID
    company_id: UUID
    product_id: UUID
    type: str
    concept: str
    quantity: Decimal
    origin_document_id: UUID | None
    notes: str | None
    created_at: datetime
    created_by: UUID
    merma: MermaResponse | None
    ajuste: AjusteInventarioResponse | None

    model_config = {
        "from_attributes": True
    }


class StockResponse(BaseModel):
    product_id: UUID
    stock: Decimal
