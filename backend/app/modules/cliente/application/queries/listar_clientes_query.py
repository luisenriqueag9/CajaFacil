from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ListarClientesQuery:
    company_id: UUID
    status: str | None = None
