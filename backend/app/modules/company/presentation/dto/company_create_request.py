from pydantic import BaseModel, Field

class CompanyCreateRequest(BaseModel):
    """DTO representing the payload required to create/register a new company."""
    business_name: str = Field(..., max_length=100, description="Legal business name")
    trade_name: str = Field(..., max_length=100, description="Commercial trade name")
    tax_id: str = Field(..., max_length=50, description="Unique Tax Identification ID")
    email: str = Field(..., max_length=100, description="Contact email address")
    phone: str | None = Field(None, max_length=20, description="Optional contact phone number")
    country: str | None = Field(None, max_length=50, description="Optional country of registration")
    currency: str = Field(..., max_length=10, description="Base currency code (e.g. USD, HNL)")
    timezone: str = Field(..., max_length=50, description="Preferred timezone name")
    status: str = Field("ACTIVE", max_length=20, description="Initial administrative status")
