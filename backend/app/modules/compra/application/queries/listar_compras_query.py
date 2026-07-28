from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ListarComprasQuery:
    company_id: UUID
    status: str | None = None
    supplier_id: UUID | None = None
