from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ObtenerClienteQuery:
    client_id: UUID
