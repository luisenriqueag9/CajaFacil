from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class ClienteRegistrado:
    client_id: UUID
    company_id: UUID
    name: str
    tax_id: str | None
    occurred_at: datetime

@dataclass(frozen=True)
class ClienteActualizado:
    client_id: UUID
    company_id: UUID
    name: str
    tax_id: str | None
    occurred_at: datetime

@dataclass(frozen=True)
class ClienteInactivado:
    client_id: UUID
    company_id: UUID
    occurred_at: datetime
