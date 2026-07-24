from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class TasaImpuestoResponse(BaseModel):
    id: UUID
    configuracion_id: UUID
    name: str
    code: str
    rate_percentage: Decimal

    model_config = {
        "from_attributes": True
    }


class ConfiguracionTributariaResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    is_active: bool
    valid_from: datetime
    valid_to: datetime | None
    calculation_type: str
    rates: list[TasaImpuestoResponse]

    model_config = {
        "from_attributes": True
    }


class DesgloseImpuestoResponse(BaseModel):
    rate_code: str
    rate_percentage: Decimal
    net_amount: Decimal
    tax_amount: Decimal

    model_config = {
        "from_attributes": True
    }
