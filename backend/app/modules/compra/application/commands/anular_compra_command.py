from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class AnularCompraCommand:
    purchase_id: UUID
    voided_by: UUID | None = None
    void_reason: str | None = None
