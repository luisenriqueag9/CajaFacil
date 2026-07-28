import uuid
from datetime import datetime
from typing import Union, List, Any
from decimal import Decimal

from app.modules.caja.domain.value_objects.estado_sesion import EstadoSesion
from app.modules.caja.domain.value_objects.tipo_movimiento import TipoMovimiento
from app.modules.caja.domain.value_objects.metodo_pago import MetodoPago
from app.modules.caja.domain.value_objects.dinero import Dinero
from app.modules.caja.domain.entities.movimiento_caja import MovimientoCaja
from app.modules.caja.domain.entities.arqueo_caja import ArqueoCaja
from app.modules.caja.domain.exceptions.caja_exceptions import (
    CajaCerradaException,
    CajaNoAbiertaException,
    MontoInvalidoException
)

class SesionCaja:
    """
    Aggregate Root que representa una Sesion o Turno de Caja.
    """
    def __init__(
        self,
        id: uuid.UUID,
        caja_id: uuid.UUID,
        company_id: uuid.UUID,
        user_id: uuid.UUID,
        status: Union[EstadoSesion, str],
        opening_balance: Union[Dinero, Decimal, int, float],
        opened_at: datetime,
        closed_at: datetime | None,
        movements: List[MovimientoCaja] = None,
        audits: List[ArqueoCaja] = None
    ):
        self.id = id
        self.caja_id = caja_id
        self.company_id = company_id
        self.user_id = user_id
        
        self.status = status if isinstance(status, EstadoSesion) else EstadoSesion(status)
        self.opening_balance = opening_balance if isinstance(opening_balance, Dinero) else Dinero(opening_balance)
        self.opened_at = opened_at
        self.closed_at = closed_at
        
        self.movements = movements if movements is not None else []
        self.audits = audits if audits is not None else []
        
        self._events: List[Any] = []
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.id, uuid.UUID):
            raise ValueError("El ID de la sesion debe ser un UUID valido.")
        if not isinstance(self.caja_id, uuid.UUID):
            raise ValueError("El ID de la caja debe ser un UUID valido.")
        if not isinstance(self.company_id, uuid.UUID):
            raise ValueError("El ID de la empresa debe ser un UUID valido.")
        if not isinstance(self.user_id, uuid.UUID):
            raise ValueError("El ID del usuario debe ser un UUID valido.")
        if self.opening_balance.monto < 0:
            raise ValueError("El fondo de apertura no puede ser negativo.")

    @property
    def eventos(self) -> List[Any]:
        return self._events

    def registrar_evento(self, evento: Any) -> None:
        self._events.append(evento)

    def limpiar_eventos(self) -> None:
        self._events.clear()

    @classmethod
    def abrir(
        cls,
        id: uuid.UUID,
        caja_id: uuid.UUID,
        company_id: uuid.UUID,
        user_id: uuid.UUID,
        opening_balance: Union[Dinero, Decimal, int, float],
        opened_at: datetime
    ) -> "SesionCaja":
        """
        Factory method para abrir una nueva sesion de caja.
        """
        balance_vo = opening_balance if isinstance(opening_balance, Dinero) else Dinero(opening_balance)
        sesion = cls(
            id=id,
            caja_id=caja_id,
            company_id=company_id,
            user_id=user_id,
            status=EstadoSesion.abierta(),
            opening_balance=balance_vo,
            opened_at=opened_at,
            closed_at=None
        )

        from app.modules.caja.domain.events.caja_events import SesionCajaAbierta
        sesion.registrar_evento(
            SesionCajaAbierta(
                sesion_id=sesion.id,
                caja_id=sesion.caja_id,
                company_id=sesion.company_id,
                user_id=sesion.user_id,
                opening_balance=sesion.opening_balance.monto,
                occurred_at=opened_at
            )
        )
        return sesion

    def registrar_movimiento(
        self,
        id: uuid.UUID,
        type: str,
        amount: Union[Dinero, Decimal, int, float],
        payment_method: str,
        concept: str,
        origin_context: str | None,
        origin_document_id: uuid.UUID | None,
        timestamp: datetime
    ) -> MovimientoCaja:
        """
        Agrega un movimiento financiero o de efectivo a la sesion de caja activa.
        """
        if self.status.is_cerrada:
            raise CajaCerradaException(self.id)

        movimiento = MovimientoCaja(
            id=id,
            sesion_id=self.id,
            type=type,
            amount=amount,
            payment_method=payment_method,
            concept=concept,
            origin_context=origin_context,
            origin_document_id=origin_document_id,
            voided=False,
            created_at=timestamp
        )
        self.movements.append(movimiento)

        from app.modules.caja.domain.events.caja_events import MovimientoCajaRegistrado
        self.registrar_evento(
            MovimientoCajaRegistrado(
                movimiento_id=movimiento.id,
                sesion_id=self.id,
                type=movimiento.type.valor,
                amount=movimiento.amount.monto,
                payment_method=movimiento.payment_method.valor,
                concept=movimiento.concept,
                occurred_at=timestamp
            )
        )
        return movimiento

    def registrar_arqueo(self, physical_amount: Union[Dinero, Decimal, int, float], supervisor_id: uuid.UUID | None, timestamp: datetime) -> ArqueoCaja:
        """
        Realiza un arqueo/auditoria en la sesion actual.
        """
        if self.status.is_cerrada:
            raise CajaCerradaException(self.id)

        physical_vo = physical_amount if isinstance(physical_amount, Dinero) else Dinero(physical_amount)

        # Calculate theoretical cash balance
        system_cash = self.opening_balance.monto
        for m in self.movements:
            if not m.voided and m.payment_method.is_efectivo:
                if m.type.is_ingreso:
                    system_cash += m.amount.monto
                elif m.type.is_egreso:
                    system_cash -= m.amount.monto

        difference = physical_vo.monto - system_cash

        audit = ArqueoCaja(
            id=uuid.uuid4(),
            sesion_id=self.id,
            physical_amount=physical_vo,
            system_amount=Dinero(system_cash, physical_vo.divisa),
            difference=Dinero(difference, physical_vo.divisa),
            supervisor_id=supervisor_id,
            created_at=timestamp
        )
        self.audits.append(audit)

        from app.modules.caja.domain.events.caja_events import ArqueoCajaRealizado
        self.registrar_evento(
            ArqueoCajaRealizado(
                sesion_id=self.id,
                physical_amount=physical_vo.monto,
                system_amount=system_cash,
                difference=difference,
                occurred_at=timestamp
            )
        )
        return audit

    def cerrar(self, closed_at: datetime) -> None:
        """
        Cierra definitivamente la sesion de caja.
        """
        if self.status.is_cerrada:
            raise CajaCerradaException(self.id)

        self.status = EstadoSesion.cerrada()
        self.closed_at = closed_at

        from app.modules.caja.domain.events.caja_events import SesionCajaCerrada
        self.registrar_evento(
            SesionCajaCerrada(
                sesion_id=self.id,
                caja_id=self.caja_id,
                closed_at=closed_at,
                occurred_at=closed_at
            )
        )

    def anular_movimiento(self, movimiento_id: uuid.UUID, timestamp: datetime) -> MovimientoCaja:
        """
        Anula un movimiento mediante contramovimiento para preservar la inmutabilidad historica.
        """
        if self.status.is_cerrada:
            raise CajaCerradaException(self.id)

        target = None
        for m in self.movements:
            if m.id == movimiento_id:
                target = m
                break

        if target is None:
            raise ValueError(f"Movimiento con ID '{movimiento_id}' no encontrado en esta sesion.")
        if target.voided:
            raise ValueError(f"El movimiento con ID '{movimiento_id}' ya se encuentra anulado.")

        # Mark original as voided
        target.anular()

        # Create contramovement
        opposite_type = "EGRESO" if target.type.is_ingreso else "INGRESO"
        contramovimiento = MovimientoCaja(
            id=uuid.uuid4(),
            sesion_id=self.id,
            type=opposite_type,
            amount=target.amount,
            payment_method=target.payment_method,
            concept=f"ANULACION - {target.concept}",
            origin_context=target.origin_context,
            origin_document_id=target.origin_document_id,
            voided=True,  # Contramovement is also marked voided so it doesn't double-affect active balances
            created_at=timestamp
        )
        self.movements.append(contramovimiento)

        from app.modules.caja.domain.events.caja_events import MovimientoCajaAnulado
        self.registrar_evento(
            MovimientoCajaAnulado(
                movimiento_id=target.id,
                sesion_id=self.id,
                concept=target.concept,
                amount=target.amount.monto,
                occurred_at=timestamp
            )
        )
        return contramovimiento
