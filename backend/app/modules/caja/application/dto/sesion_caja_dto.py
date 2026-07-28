from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List

from app.modules.caja.application.dto.movimiento_caja_dto import MovimientoCajaDTO
from app.modules.caja.application.dto.arqueo_caja_dto import ArqueoCajaDTO

@dataclass(frozen=True)
class SesionCajaDTO:
    id: UUID
    caja_id: UUID
    company_id: UUID
    user_id: UUID
    status: str
    opening_balance: Decimal
    opened_at: datetime
    closed_at: datetime | None
    movements: List[MovimientoCajaDTO]
    audits: List[ArqueoCajaDTO]
