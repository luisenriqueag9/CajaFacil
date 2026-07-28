from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class RegistrarClienteCommand:
    company_id: UUID
    name: str
    tax_id: str | None
    phone: str | None
    email: str | None
