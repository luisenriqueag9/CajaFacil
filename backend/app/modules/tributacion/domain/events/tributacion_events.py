from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class ConfiguracionTributariaCreada:
    configuracion_id: UUID
    company_id: UUID
    valid_from: datetime
    occurred_at: datetime


@dataclass(frozen=True)
class ConfiguracionTributariaActivada:
    configuracion_id: UUID
    company_id: UUID
    valid_from: datetime
    occurred_at: datetime


@dataclass(frozen=True)
class ConfiguracionTributariaDesactivada:
    configuracion_id: UUID
    company_id: UUID
    valid_to: datetime
    occurred_at: datetime
