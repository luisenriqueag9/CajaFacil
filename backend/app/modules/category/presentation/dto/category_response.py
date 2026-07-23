from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class CategoryResponse(BaseModel):
    """DTO representing the data payload returned to clients containing category details."""
    id: UUID
    company_id: UUID
    name: str = Field(..., max_length=100)
    status: str = Field(..., max_length=20)
    protected: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
