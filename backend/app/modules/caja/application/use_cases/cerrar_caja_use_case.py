import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.caja.domain.entities.caja import Caja, ArqueoCaja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.exceptions import CajaNotFoundException
from app.modules.caja.domain.events.caja_events import CajaCerrada
from app.modules.caja.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class CerrarCajaCommand:
    company_id: uuid.UUID
    caja_id: uuid.UUID
    physical_amount: Decimal
    supervisor_id: uuid.UUID | None = None

class CerrarCajaUseCase:
    """
    Application Use Case to finalize and close a Cash Register session.
    Requires final physical cash audit and freezes the session state.
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

    def execute(self, command: CerrarCajaCommand) -> Caja:
        # 1. Fetch session
        caja = self.repository.get_by_id(command.caja_id)
        if caja is None or caja.company_id != command.company_id:
            raise CajaNotFoundException(command.caja_id)

        # 2. Derive expected cash balance in system (EFECTIVO movements only)
        system_amount = Decimal("0.0000")
        for m in caja.movements:
            if m.payment_method == "EFECTIVO":
                if m.type == "INGRESO":
                    system_amount += m.amount
                elif m.type == "EGRESO":
                    system_amount -= m.amount

        # 3. Calculate difference
        difference = command.physical_amount - system_amount

        # 4. Construct final closing audit entity
        now = datetime.now(timezone.utc)
        arqueo_final = ArqueoCaja(
            id=uuid.uuid4(),
            caja_id=caja.id,
            physical_amount=command.physical_amount,
            system_amount=system_amount,
            difference=difference,
            created_at=now,
            supervisor_id=command.supervisor_id
        )

        # 5. Transition aggregate state to CERRADA
        caja.cerrar(now, arqueo_final)

        # 6. Save and Dispatch (Unit of Work)
        try:
            with self.db.begin_nested():
                saved_caja = self.repository.save(caja)
                
                event = CajaCerrada(
                    caja_id=saved_caja.id,
                    company_id=saved_caja.company_id,
                    physical_amount=arqueo_final.physical_amount,
                    system_amount=arqueo_final.system_amount,
                    difference=arqueo_final.difference,
                    occurred_at=now
                )
                self.event_dispatcher.dispatch(event)
            self.db.commit()
            return saved_caja
        except Exception as e:
            self.db.rollback()
            raise e
