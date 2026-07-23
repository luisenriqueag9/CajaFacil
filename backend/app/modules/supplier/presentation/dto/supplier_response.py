from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class SupplierResponse(BaseModel):
    """DTO representing the data payload returned containing supplier details."""
    id: UUID
    company_id: UUID
    name: str = Field(..., max_length=100)
    tax_id: str | None = Field(None, max_length=50)
    contact_name: str | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=50)
    email: str | None = Field(None, max_length=100)
    status: str = Field(..., max_length=20)
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
