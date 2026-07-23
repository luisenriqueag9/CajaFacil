from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.modules.caja.domain.exceptions import (
    CajaCerradaException, 
    CajaNoAbiertaException, 
    MontoInvalidoException
)

@dataclass
class MovimientoCaja:
    id: UUID
    caja_id: UUID
    type: str  # INGRESO, EGRESO
    amount: Decimal
    payment_method: str  # EFECTIVO, TARJETA, TRANSFERENCIA, CREDITO
    concept: str  # VENTA, COMPRA, RETIRO, GASTO, ABONO_CREDITO, FONDO_APERTURA, AJUSTE_ARQUEO
    origin_document_id: UUID | None
    created_at: datetime

    def __post_init__(self) -> None:
        if self.amount <= Decimal("0.0000"):
            raise MontoInvalidoException(float(self.amount))
        if self.type not in {"INGRESO", "EGRESO"}:
            raise ValueError(f"Tipo de movimiento de caja inválido: {self.type}")
        valid_methods = {"EFECTIVO", "TARJETA", "TRANSFERENCIA", "CREDITO"}
        if self.payment_method not in valid_methods:
            raise ValueError(f"Método de pago inválido: {self.payment_method}")
        valid_concepts = {"VENTA", "COMPRA", "RETIRO", "GASTO", "ABONO_CREDITO", "FONDO_APERTURA", "AJUSTE_ARQUEO"}
        if self.concept not in valid_concepts:
            raise ValueError(f"Concepto de movimiento de caja inválido: {self.concept}")


@dataclass
class ArqueoCaja:
    id: UUID
    caja_id: UUID
    physical_amount: Decimal
    system_amount: Decimal
    difference: Decimal
    created_at: datetime
    supervisor_id: UUID | None = None


@dataclass
class Caja:
    id: UUID
    company_id: UUID
    user_id: UUID
    status: str  # ABIERTA, CERRADA
    opening_balance: Decimal
    opened_at: datetime
    closed_at: datetime | None = None
    movements: list[MovimientoCaja] = field(default_factory=list)
    audits: list[ArqueoCaja] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in {"ABIERTA", "CERRADA"}:
            raise ValueError(f"Estado de caja inválido: {self.status}")

    def agregar_movimiento(self, movimiento: MovimientoCaja) -> None:
        if self.status == "CERRADA":
            raise CajaCerradaException(self.id)
        self.movements.append(movimiento)

    def agregar_arqueo(self, arqueo: ArqueoCaja) -> None:
        if self.status == "CERRADA":
            raise CajaCerradaException(self.id)
        self.audits.append(arqueo)

    def cerrar(self, closed_at: datetime, arqueo_final: ArqueoCaja) -> None:
        if self.status == "CERRADA":
            raise CajaCerradaException(self.id)
        if self.status != "ABIERTA":
            raise CajaNoAbiertaException(self.id)
        self.status = "CERRADA"
        self.closed_at = closed_at
        # Add the final audit directly bypass status block inside agregator
        self.audits.append(arqueo_final)
