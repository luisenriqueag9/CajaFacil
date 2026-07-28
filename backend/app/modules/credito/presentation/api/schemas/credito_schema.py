from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class AbrirCuentaCreditoRequest(BaseModel):
    company_id: UUID
    client_id: UUID
    credit_limit: Decimal = Field(..., gt=0)

class ActualizarLimiteCreditoRequest(BaseModel):
    new_limit: Decimal = Field(..., gt=0)

class CreditoResponse(BaseModel):
    id: UUID
    company_id: UUID
    client_id: UUID
    credit_limit: Decimal
    balance: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
