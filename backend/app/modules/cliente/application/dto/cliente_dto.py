from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class ClienteDTO:
    id: UUID
    company_id: UUID
    name: str
    tax_id: str | None
    phone: str | None
    email: str | None
    status: str
    created_at: datetime
    updated_at: datetime
