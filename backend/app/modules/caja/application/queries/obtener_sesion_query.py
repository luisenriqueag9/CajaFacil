from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ObtenerSesionQuery:
    sesion_id: UUID
