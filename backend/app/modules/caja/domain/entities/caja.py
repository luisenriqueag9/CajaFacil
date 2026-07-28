from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Caja:
    id: UUID
    company_id: UUID
    name: str
    status: str  # ACTIVA, INACTIVA
    created_at: datetime
