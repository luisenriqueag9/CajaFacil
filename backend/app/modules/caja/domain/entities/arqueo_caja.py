from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from app.modules.caja.domain.value_objects.dinero import Dinero

@dataclass
class ArqueoCaja:
    id: UUID
    sesion_id: UUID
    physical_amount: Dinero
    system_amount: Dinero
    difference: Dinero
    supervisor_id: UUID | None
    created_at: datetime
