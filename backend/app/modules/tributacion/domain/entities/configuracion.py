from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.modules.tributacion.domain.exceptions import (
    ConfiguracionInvalidaException,
    ConfiguracionExpiradaException
)

@dataclass(frozen=True)
class DesgloseImpuesto:
    rate_code: str
    rate_percentage: Decimal
    net_amount: Decimal
    tax_amount: Decimal


@dataclass
class TasaImpuesto:
    id: UUID
    configuracion_id: UUID
    name: str
    code: str
    rate_percentage: Decimal

    def __post_init__(self) -> None:
        if self.rate_percentage < Decimal("0.0000"):
            raise ConfiguracionInvalidaException("El porcentaje de tasa impositiva no puede ser negativo.")
        if not self.name or not self.name.strip():
            raise ConfiguracionInvalidaException("El nombre de la tasa impositiva no puede estar vacío.")
        if not self.code or not self.code.strip():
            raise ConfiguracionInvalidaException("El código de la tasa impositiva no puede estar vacío.")


@dataclass
class ConfiguracionTributaria:
    id: UUID
    company_id: UUID
    name: str
    is_active: bool
    valid_from: datetime
    valid_to: datetime | None = None
    calculation_type: str = "ADICIONADO"  # INCLUIDO, ADICIONADO
    rates: list[TasaImpuesto] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ConfiguracionInvalidaException("El nombre de la configuración no puede estar vacío.")
        if self.calculation_type not in {"INCLUIDO", "ADICIONADO"}:
            raise ConfiguracionInvalidaException(
                f"Tipo de cálculo impositivo '{self.calculation_type}' inválido. Valores permitidos: INCLUIDO, ADICIONADO"
            )

    def agregar_tasa(self, tasa: TasaImpuesto) -> None:
        if self.valid_to is not None and self.valid_to < datetime.now(self.valid_to.tzinfo):
            raise ConfiguracionExpiradaException(self.id)
        
        # Check unique codes in rates
        for r in self.rates:
            if r.code == tasa.code:
                raise ConfiguracionInvalidaException(f"El código de tasa '{tasa.code}' ya existe en esta configuración.")
        
        self.rates.append(tasa)

    def desactivar(self, valid_to: datetime) -> None:
        self.is_active = False
        self.valid_to = valid_to

    def activar(self, valid_from: datetime) -> None:
        self.is_active = True
        self.valid_from = valid_from
        self.valid_to = None
