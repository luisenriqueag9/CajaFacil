from pydantic import BaseModel, Field


class CompanyUpdateRequest(BaseModel):
    """DTO representing the payload used to update an existing company's modifiable fields."""

    business_name: str | None = Field(None, max_length=100)
    trade_name: str | None = Field(None, max_length=100)
    email: str | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    currency: str | None = Field(None, max_length=10)
    timezone: str | None = Field(None, max_length=50)
    status: str | None = Field(None, max_length=20)