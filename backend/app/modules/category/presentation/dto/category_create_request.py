from uuid import UUID
from pydantic import BaseModel, Field

class CategoryCreateRequest(BaseModel):
    """DTO representing the payload required to create a new category."""
    company_id: UUID = Field(..., description="ID of the company that owns this category")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the category")
    status: str = Field("ACTIVO", max_length=20, description="Initial status of the category")
