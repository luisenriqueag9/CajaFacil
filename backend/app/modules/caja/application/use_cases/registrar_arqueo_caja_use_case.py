import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.caja.domain.entities.caja import ArqueoCaja, MovimientoCaja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.exceptions import CajaNotFoundException
from app.modules.caja.domain.events.caja_events import ArqueoRealizado
from app.modules.caja.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class RegistrarArqueoCajaCommand:
    company_id: uuid.UUID
    caja_id: uuid.UUID
    physical_amount: Decimal
    supervisor_id: uuid.UUID | None = None

class RegistrarArqueoCajaUseCase:
    """
    Application Use Case to perform a Cash Box audit (Arqueo).
    Calculates expected cash based on EFECTIVO movements and logs differences.
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

    def execute(self, command: RegistrarArqueoCajaCommand) -> ArqueoCaja:
        # 1. Fetch box session
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

        # 4. Construct domain entities
        now = datetime.now(timezone.utc)
        arqueo_id = uuid.uuid4()
        arqueo = ArqueoCaja(
            id=arqueo_id,
            caja_id=caja.id,
            physical_amount=command.physical_amount,
            system_amount=system_amount,
            difference=difference,
            created_at=now,
            supervisor_id=command.supervisor_id
        )

        caja.agregar_arqueo(arqueo)

        # 5. Optional: Register corrective adjustment movement to align logical stock
        if difference != Decimal("0.0000"):
            adj_type = "INGRESO" if difference > Decimal("0.0000") else "EGRESO"
            adj_amount = abs(difference)
            
            adjust_mov = MovimientoCaja(
                id=uuid.uuid4(),
                caja_id=caja.id,
                type=adj_type,
                amount=adj_amount,
                payment_method="EFECTIVO",
                concept="AJUSTE_ARQUEO",
                origin_document_id=arqueo_id,
                created_at=now
            )
            caja.agregar_movimiento(adjust_mov)

        # 6. Save and Dispatch (Unit of Work)
        try:
            with self.db.begin_nested():
                self.repository.save(caja)
                
                event = ArqueoRealizado(
                    arqueo_id=arqueo.id,
                    caja_id=caja.id,
                    company_id=caja.company_id,
                    physical_amount=arqueo.physical_amount,
                    difference=arqueo.difference,
                    occurred_at=arqueo.created_at
                )
                self.event_dispatcher.dispatch(event)
            self.db.commit()
            return arqueo
        except Exception as e:
            self.db.rollback()
            raise e
