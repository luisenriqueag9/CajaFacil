import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.caja.domain.entities.caja import Caja, MovimientoCaja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.exceptions import CajaYaAbiertaException
from app.modules.caja.domain.events.caja_events import CajaAbierta
from app.modules.caja.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class AbrirCajaCommand:
    company_id: uuid.UUID
    user_id: uuid.UUID
    opening_balance: Decimal

class AbrirCajaUseCase:
    """
    Application Use Case to open a new Cash Register session for a cashier.
    Enforces custody rules and initializes base funds.
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

    def execute(self, command: AbrirCajaCommand) -> Caja:
        # 1. Enforce custody rule: user cannot have more than one open box session
        active_box = self.repository.get_active_by_user(command.company_id, command.user_id)
        if active_box is not None:
            raise CajaYaAbiertaException(command.user_id)

        # 2. Construct Caja aggregate root
        caja_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        caja = Caja(
            id=caja_id,
            company_id=command.company_id,
            user_id=command.user_id,
            status="ABIERTA",
            opening_balance=command.opening_balance,
            opened_at=now,
            movements=[]
        )

        # 3. Create initial opening balance movement if base funds > 0
        if command.opening_balance > Decimal("0.0000"):
            init_mov = MovimientoCaja(
                id=uuid.uuid4(),
                caja_id=caja_id,
                type="INGRESO",
                amount=command.opening_balance,
                payment_method="EFECTIVO",
                concept="FONDO_APERTURA",
                origin_document_id=None,
                created_at=now
            )
            caja.agregar_movimiento(init_mov)

        # 4. Save and Dispatch (Unit of Work)
        try:
            with self.db.begin_nested():
                saved_caja = self.repository.save(caja)
                
                event = CajaAbierta(
                    caja_id=saved_caja.id,
                    company_id=saved_caja.company_id,
                    user_id=saved_caja.user_id,
                    opening_balance=saved_caja.opening_balance,
                    occurred_at=saved_caja.opened_at
                )
                self.event_dispatcher.dispatch(event)
            self.db.commit()
            return saved_caja
        except Exception as e:
            self.db.rollback()
            raise e
