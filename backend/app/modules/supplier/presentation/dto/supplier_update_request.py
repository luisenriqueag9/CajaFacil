from pydantic import BaseModel, Field

class SupplierUpdateRequest(BaseModel):
    """DTO representing the payload required to update an existing supplier."""
    name: str | None = Field(None, min_length=1, max_length=100, description="New name for the supplier")
    tax_id: str | None = Field(None, max_length=50, description="New tax identifier (optional)")
    contact_name: str | None = Field(None, max_length=100, description="New contact person name (optional)")
    phone: str | None = Field(None, max_length=50, description="New phone number (optional)")
    email: str | None = Field(None, max_length=100, description="New email address (optional)")
