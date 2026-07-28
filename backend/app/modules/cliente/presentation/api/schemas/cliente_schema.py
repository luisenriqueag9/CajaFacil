from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class RegistrarClienteRequest(BaseModel):
    company_id: UUID
    name: str = Field(min_length=2, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)

class ActualizarClienteRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)

class ClienteResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    tax_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
