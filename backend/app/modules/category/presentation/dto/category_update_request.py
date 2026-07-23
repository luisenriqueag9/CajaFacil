from pydantic import BaseModel, Field

class CategoryUpdateRequest(BaseModel):
    """DTO representing the payload required to update an existing category."""
    name: str | None = Field(None, min_length=1, max_length=100, description="New name for the category")
    status: str | None = Field(None, max_length=20, description="New status for the category")
