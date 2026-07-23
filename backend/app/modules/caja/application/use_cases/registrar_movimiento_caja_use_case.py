import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.caja.domain.entities.caja import MovimientoCaja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.exceptions import CajaNotFoundException
from app.modules.caja.domain.events.caja_events import MovimientoCajaRegistrado
from app.modules.caja.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class RegistrarMovimientoCajaCommand:
    company_id: uuid.UUID
    caja_id: uuid.UUID
    type: str  # INGRESO, EGRESO
    amount: Decimal
    payment_method: str  # EFECTIVO, TARJETA, TRANSFERENCIA, CREDITO
    concept: str  # VENTA, COMPRA, RETIRO, GASTO, ABONO_CREDITO, FONDO_APERTURA, AJUSTE_ARQUEO
    origin_document_id: uuid.UUID | None = None

class RegistrarMovimientoCajaUseCase:
    """
    Application Use Case to record a cash flow movement (income or expense)
    associated with an open Cash Register session.
    """
    def __init__(
        self,
        repository: CajaRepository,
        db: Session,
        event_dispatcher: EventDispatcher
    ):
        self.repository = repository
        self.db = db
        self.event_dispatcher = event_dispatcher

    def execute(self, command: RegistrarMovimientoCajaCommand) -> MovimientoCaja:
        # 1. Fetch box session
        caja = self.repository.get_by_id(command.caja_id)
        if caja is None or caja.company_id != command.company_id:
            raise CajaNotFoundException(command.caja_id)

        # 2. Construct domain entity (runs validations)
        now = datetime.now(timezone.utc)
        movimiento = MovimientoCaja(
            id=uuid.uuid4(),
            caja_id=caja.id,
            type=command.type,
            amount=command.amount,
            payment_method=command.payment_method,
            concept=command.concept,
            origin_document_id=command.origin_document_id,
            created_at=now
        )

        # 3. Add to aggregate root (validates open state)
        caja.agregar_movimiento(movimiento)

        # 4. Save and Dispatch (Unit of Work)
        try:
            with self.db.begin_nested():
                self.repository.save(caja)
                
                event = MovimientoCajaRegistrado(
                    movimiento_id=movimiento.id,
                    caja_id=caja.id,
                    company_id=caja.company_id,
                    amount=movimiento.amount,
                    type=movimiento.type,
                    concept=movimiento.concept,
                    occurred_at=movimiento.created_at
                )
                self.event_dispatcher.dispatch(event)
            self.db.commit()
            return movimiento
        except Exception as e:
            self.db.rollback()
            raise e
