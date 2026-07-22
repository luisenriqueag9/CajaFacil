from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Company:
    id: UUID
    business_name: str
    trade_name: str
    tax_id: str
    email: str
    phone: str | None
    country: str | None
    currency: str
    timezone: str
    status: str
    created_at: datetime
    updated_at: datetime

    def update_profile(
        self,
        *,
        business_name: str,
        trade_name: str,
        email: str,
        phone: str | None,
        currency: str,
        timezone: str,
        status: str,
    ) -> None:
        """
        Updates the company's modifiable details with explicit and typed parameters.
        """
        self.business_name = business_name
        self.trade_name = trade_name
        self.email = email
        self.phone = phone
        self.currency = currency
        self.timezone = timezone
        self.status = status

