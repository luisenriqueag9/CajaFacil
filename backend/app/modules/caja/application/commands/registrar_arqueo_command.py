from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class RegistrarArqueoCommand:
    sesion_id: UUID
    physical_amount: Decimal
    supervisor_id: UUID | None = None
