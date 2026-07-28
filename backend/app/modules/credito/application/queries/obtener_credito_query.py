from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ObtenerCreditoQuery:
    credit_id: UUID
