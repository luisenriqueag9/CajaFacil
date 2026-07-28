from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class InactivarClienteCommand:
    client_id: UUID
