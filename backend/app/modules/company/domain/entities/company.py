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
