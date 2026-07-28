from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ListarSesionesQuery:
    company_id: UUID
    status: str | None = None
