from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class CerrarSesionCommand:
    sesion_id: UUID
