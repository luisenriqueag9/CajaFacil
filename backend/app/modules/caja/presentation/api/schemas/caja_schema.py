from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

class AbrirSesionRequest(BaseModel):
    caja_id: UUID
    company_id: UUID
    user_id: UUID
    opening_balance: Decimal = Field(..., ge=0)

class RegistrarMovimientoRequest(BaseModel):
    type: str = Field(..., pattern="^(INGRESO|EGRESO)$")
    amount: Decimal = Field(..., gt=0)
    payment_method: str = Field(..., pattern="^(EFECTIVO|TARJETA|TRANSFERENCIA|CREDITO)$")
    concept: str = Field(..., min_length=2, max_length=100)
    origin_context: Optional[str] = Field(None, max_length=50)
    origin_document_id: Optional[UUID] = None

class RegistrarArqueoRequest(BaseModel):
    physical_amount: Decimal = Field(..., ge=0)
    supervisor_id: Optional[UUID] = None

class MovimientoResponse(BaseModel):
    id: UUID
    sesion_id: UUID
    type: str
    amount: Decimal
    payment_method: str
    concept: str
    origin_context: Optional[str] = None
    origin_document_id: Optional[UUID] = None
    voided: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class ArqueoResponse(BaseModel):
    id: UUID
    sesion_id: UUID
    physical_amount: Decimal
    system_amount: Decimal
    difference: Decimal
    supervisor_id: Optional[UUID] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class SesionResponse(BaseModel):
    id: UUID
    caja_id: UUID
    company_id: UUID
    user_id: UUID
    status: str
    opening_balance: Decimal
    opened_at: datetime
    closed_at: Optional[datetime] = None
    movements: List[MovimientoResponse]
    audits: List[ArqueoResponse]

    model_config = {"from_attributes": True}
