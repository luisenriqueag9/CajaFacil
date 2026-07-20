from pydantic import BaseModel, Field

class CompanyUpdateRequest(BaseModel):
    """DTO representing the payload used to update an existing company's modifiable fields."""
    business_name: str | None = Field(None, max_length=100, description="Updated business name")
    trade_name: str | None = Field(None, max_length=100, description="Updated trade name")
    tax_id: str | None = Field(None, max_length=50, description="Updated Tax ID")
    email: str | None = Field(None, max_length=100, description="Updated email address")
    phone: str | None = Field(None, max_length=20, description="Updated phone number")
    country: str | None = Field(None, max_length=50, description="Updated country")
    currency: str | None = Field(None, max_length=10, description="Updated base currency")
    timezone: str | None = Field(None, max_length=50, description="Updated timezone")
    status: str | None = Field(None, max_length=20, description="Updated status")
