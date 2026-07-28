from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class AnularMovimientoCommand:
    sesion_id: UUID
    movimiento_id: UUID
