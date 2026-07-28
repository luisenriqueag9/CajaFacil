from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ListarCreditosQuery:
    company_id: UUID
    status: str | None = None
