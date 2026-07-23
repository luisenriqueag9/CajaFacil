from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class MovimientoCajaResponse(BaseModel):
    id: UUID
    caja_id: UUID
    type: str
    amount: Decimal
    payment_method: str
    concept: str
    origin_document_id: UUID | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ArqueoCajaResponse(BaseModel):
    id: UUID
    caja_id: UUID
    physical_amount: Decimal
    system_amount: Decimal
    difference: Decimal
    created_at: datetime
    supervisor_id: UUID | None

    model_config = {
        "from_attributes": True
    }


class CajaResponse(BaseModel):
    id: UUID
    company_id: UUID
    user_id: UUID
    status: str
    opening_balance: Decimal
    opened_at: datetime
    closed_at: datetime | None
    movements: list[MovimientoCajaResponse]
    audits: list[ArqueoCajaResponse]

    model_config = {
        "from_attributes": True
    }


class SaldoBreakdownResponse(BaseModel):
    expected_cash: Decimal
    expected_card: Decimal
    expected_transfer: Decimal
    expected_credit: Decimal
    total: Decimal
