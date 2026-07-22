from pydantic import BaseModel, Field

class BrandUpdateRequest(BaseModel):
    """DTO representing the payload required to update an existing brand."""
    name: str | None = Field(None, min_length=1, max_length=100, description="New name for the brand")
    status: str | None = Field(None, max_length=20, description="New status for the brand")
