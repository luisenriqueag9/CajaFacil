from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class CompanyResponse(BaseModel):
    """DTO representing the data payload returned to clients containing all company details."""
    id: UUID
    business_name: str = Field(..., max_length=100)
    trade_name: str = Field(..., max_length=100)
    tax_id: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    phone: str | None = Field(None, max_length=20)
    country: str | None = Field(None, max_length=50)
    currency: str = Field(..., max_length=10)
    timezone: str = Field(..., max_length=50)
    status: str = Field(..., max_length=20)
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True  # Enable compatibility with arbitrary objects/ORMs
    }
