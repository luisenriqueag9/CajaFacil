from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Union

from app.modules.caja.domain.value_objects.tipo_movimiento import TipoMovimiento
from app.modules.caja.domain.value_objects.metodo_pago import MetodoPago
from app.modules.caja.domain.value_objects.dinero import Dinero
from app.modules.caja.domain.exceptions.caja_exceptions import MontoInvalidoException

@dataclass
class MovimientoCaja:
    id: UUID
    sesion_id: UUID
    type: Union[TipoMovimiento, str]
    amount: Union[Dinero, Decimal, int, float]
    payment_method: Union[MetodoPago, str]
    concept: str
    origin_context: str | None
    origin_document_id: UUID | None
    voided: bool
    created_at: datetime

    def __post_init__(self) -> None:
        self.type = self.type if isinstance(self.type, TipoMovimiento) else TipoMovimiento(self.type)
        self.amount = self.amount if isinstance(self.amount, Dinero) else Dinero(self.amount)
        self.payment_method = self.payment_method if isinstance(self.payment_method, MetodoPago) else MetodoPago(self.payment_method)
        
        if not self.concept or not isinstance(self.concept, str) or not self.concept.strip():
            raise ValueError("El concepto del movimiento es obligatorio.")
        
        if self.amount.monto <= 0:
            raise MontoInvalidoException(float(self.amount.monto))

    def anular(self) -> None:
        self.voided = True
