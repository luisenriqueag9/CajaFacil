import uuid
from datetime import datetime
from typing import Union, List, Any

from app.modules.credito.domain.value_objects.estado_credito import EstadoCredito
from app.modules.credito.domain.value_objects.dinero import Dinero
from app.modules.credito.domain.exceptions.credito_invalido_exception import CreditoInvalidoException
from app.modules.credito.domain.exceptions.limite_excedido_exception import LimiteExcedidoException

class Credito:
    """
    Aggregate Root que representa una cuenta o linea de credito de un cliente.
    """
    def __init__(
        self,
        id: uuid.UUID,
        company_id: uuid.UUID,
        client_id: uuid.UUID,
        credit_limit: Union[Dinero, Decimal, int, float],
        balance: Union[Dinero, Decimal, int, float],
        status: Union[EstadoCredito, str],
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.company_id = company_id
        self.client_id = client_id
        
        self.credit_limit = credit_limit if isinstance(credit_limit, Dinero) else Dinero(credit_limit)
        self.balance = balance if isinstance(balance, Dinero) else Dinero(balance)
        self.status = status if isinstance(status, EstadoCredito) else EstadoCredito(status)
        
        self.created_at = created_at
        self.updated_at = updated_at
        self._events: List[Any] = []
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.id, uuid.UUID):
            raise CreditoInvalidoException("El ID del credito debe ser un UUID valido.")
        if not isinstance(self.company_id, uuid.UUID):
            raise CreditoInvalidoException("El ID de la empresa debe ser un UUID valido.")
        if not isinstance(self.client_id, uuid.UUID):
            raise CreditoInvalidoException("El ID del cliente debe ser un UUID valido.")
        if self.credit_limit.monto < 0:
            raise CreditoInvalidoException("El limite de credito no puede ser negativo.")
        if self.balance.monto < 0:
            raise CreditoInvalidoException("El saldo deudor no puede ser negativo.")

    @property
    def eventos(self) -> List[Any]:
        return self._events

    def registrar_evento(self, evento: Any) -> None:
        self._events.append(evento)

    def limpiar_eventos(self) -> None:
        self._events.clear()

    @classmethod
    def open_account(
        cls,
        id: uuid.UUID,
        company_id: uuid.UUID,
        client_id: uuid.UUID,
        credit_limit: Union[Dinero, Decimal, int, float],
        created_at: datetime,
        updated_at: datetime
    ) -> "Credito":
        """
        Factory method para abrir una nueva cuenta de credito en estado ACTIVO y saldo 0.
        """
        limit_vo = credit_limit if isinstance(credit_limit, Dinero) else Dinero(credit_limit)
        credito = cls(
            id=id,
            company_id=company_id,
            client_id=client_id,
            credit_limit=limit_vo,
            balance=Dinero.cero(limit_vo.divisa),
            status=EstadoCredito.activo(),
            created_at=created_at,
            updated_at=updated_at
        )

        from app.modules.credito.domain.events.credito_events import CuentaCreditoAbierta
        credito.registrar_evento(
            CuentaCreditoAbierta(
                credit_id=credito.id,
                company_id=credito.company_id,
                client_id=credito.client_id,
                credit_limit=credito.credit_limit.monto,
                occurred_at=created_at
            )
        )
        return credito

    def add_debt(self, amount: Union[Dinero, Decimal, int, float], reference_id: uuid.UUID, timestamp: datetime) -> None:
        """
        Registra una deuda/cargo en la cuenta de credito, verificando que no exceda el limite disponible.
        """
        if not self.status.is_activo:
            raise CreditoInvalidoException("La cuenta de credito no se encuentra activa.")

        amount_vo = amount if isinstance(amount, Dinero) else Dinero(amount)
        new_balance = self.balance + amount_vo

        if new_balance > self.credit_limit:
            raise LimiteExcedidoException(
                f"El cargo solicitado ({amount_vo.monto}) excede el cupo disponible del cliente. "
                f"Limite: {self.credit_limit.monto}, Saldo Actual: {self.balance.monto}."
            )

        self.balance = new_balance
        self.updated_at = timestamp
        self.validate()

        from app.modules.credito.domain.events.credito_events import DeudaRegistrada
        self.registrar_evento(
            DeudaRegistrada(
                credit_id=self.id,
                company_id=self.company_id,
                client_id=self.client_id,
                amount=amount_vo.monto,
                reference_id=reference_id,
                occurred_at=timestamp
            )
        )

    def release_debt(self, amount: Union[Dinero, Decimal, int, float], reference_id: uuid.UUID, timestamp: datetime) -> None:
        """
        Libera/reversa una deuda (por abono o devolucion).
        """
        amount_vo = amount if isinstance(amount, Dinero) else Dinero(amount)
        
        if amount_vo > self.balance:
            raise CreditoInvalidoException(
                f"El monto a liberar ({amount_vo.monto}) supera el saldo deudor actual ({self.balance.monto})."
            )

        self.balance = self.balance - amount_vo
        self.updated_at = timestamp
        self.validate()

        from app.modules.credito.domain.events.credito_events import DeudaReversada
        self.registrar_evento(
            DeudaReversada(
                credit_id=self.id,
                company_id=self.company_id,
                client_id=self.client_id,
                amount=amount_vo.monto,
                reference_id=reference_id,
                occurred_at=timestamp
            )
        )

    def update_limit(self, new_limit: Union[Dinero, Decimal, int, float], timestamp: datetime) -> None:
        """
        Modifica el limite de credito autorizado.
        """
        limit_vo = new_limit if isinstance(new_limit, Dinero) else Dinero(new_limit)
        
        # El nuevo limite no puede ser inferior al saldo deudor actual
        if limit_vo < self.balance:
            raise CreditoInvalidoException(
                f"El nuevo limite de credito ({limit_vo.monto}) no puede ser inferior al saldo deudor actual ({self.balance.monto})."
            )

        old_limit = self.credit_limit.monto
        self.credit_limit = limit_vo
        self.updated_at = timestamp
        self.validate()

        from app.modules.credito.domain.events.credito_events import LimiteCreditoActualizado
        self.registrar_evento(
            LimiteCreditoActualizado(
                credit_id=self.id,
                company_id=self.company_id,
                client_id=self.client_id,
                old_limit=old_limit,
                new_limit=self.credit_limit.monto,
                occurred_at=timestamp
            )
        )

    def suspend(self, timestamp: datetime) -> None:
        """
        Suspende la cuenta de credito impidiendo nuevos cargos.
        """
        if self.status.is_suspendido:
            raise CreditoInvalidoException("La cuenta de credito ya se encuentra suspendida.")

        self.status = EstadoCredito.suspendido()
        self.updated_at = timestamp
        self.validate()

        from app.modules.credito.domain.events.credito_events import CuentaCreditoInactivada
        self.registrar_evento(
            CuentaCreditoInactivada(
                credit_id=self.id,
                company_id=self.company_id,
                client_id=self.client_id,
                occurred_at=timestamp
            )
        )

    def activate(self, timestamp: datetime) -> None:
        """
        Activa una cuenta de credito previamente suspendida.
        """
        if self.status.is_activo:
            raise CreditoInvalidoException("La cuenta de credito ya se encuentra activa.")

        self.status = EstadoCredito.activo()
        self.updated_at = timestamp
        self.validate()
