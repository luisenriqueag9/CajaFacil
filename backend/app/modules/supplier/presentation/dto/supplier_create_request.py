from uuid import UUID
from pydantic import BaseModel, Field

class SupplierCreateRequest(BaseModel):
    """DTO representing the payload required to register a new supplier."""
    company_id: UUID = Field(..., description="ID of the company that owns this supplier")
    name: str = Field(..., min_length=1, max_length=100, description="Name of the supplier")
    tax_id: str | None = Field(None, max_length=50, description="Legal tax identifier (optional)")
    contact_name: str | None = Field(None, max_length=100, description="Contact person name (optional)")
    phone: str | None = Field(None, max_length=50, description="Contact phone number (optional)")
    email: str | None = Field(None, max_length=100, description="Contact email address (optional)")
