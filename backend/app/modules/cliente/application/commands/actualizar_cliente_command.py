from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ActualizarClienteCommand:
    client_id: UUID
    name: str
    tax_id: str | None
    phone: str | None
    email: str | None
