from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session

from app.modules.venta.domain.entities.venta import Venta
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.domain.exceptions import VentaNotFoundException
from app.modules.venta.domain.events.venta_events import VentaAnulada
from app.modules.venta.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class AnularVentaCommand:
    venta_id: UUID
    supervisor_id: UUID
    reason: str

class AnularVentaUseCase:
    """
    Application Use Case to annul/cancel a previously confirmed Venta.
    Coordinates the transaction across Venta, Inventory, Cash Box, and Credit.
    """
    def __init__(
        self,
        repository: VentaRepository,
        db: Session,
        event_dispatcher: EventDispatcher
    ):
        self.repository = repository
        self.db = db
        self.event_dispatcher = event_dispatcher

    def execute(self, command: AnularVentaCommand) -> Venta:
        # 1. Fetch the sale
        venta = self.repository.get_by_id(command.venta_id)
        if venta is None:
            raise VentaNotFoundException(command.venta_id)

        # 2. Transition to ANULADA (Domain validations will be executed inside entities/venta.py)
        now = datetime.now(timezone.utc)
        venta.anular(
            supervisor_id=command.supervisor_id,
            reason=command.reason,
            timestamp=now
        )

        # 3. Unit of Work coordination (Single SQLite transaction)
        try:
            with self.db.begin_nested():
                # Persist updated status
                updated_venta = self.repository.save(venta)

                # Prepare event payload
                items_payload = [
                    {
                        "product_id": d.product_id,
                        "quantity": d.quantity
                    } for d in updated_venta.details
                ]
                cash_amount = sum(p.amount for p in updated_venta.payments if p.payment_method == "EFECTIVO")
                credit_amount = sum(p.amount for p in updated_venta.payments if p.payment_method == "CREDITO")

                event = VentaAnulada(
                    venta_id=updated_venta.id,
                    company_id=updated_venta.company_id,
                    box_id=updated_venta.box_id,
                    client_id=updated_venta.client_id,
                    total=updated_venta.total,
                    items=items_payload,
                    cash_amount=cash_amount,
                    credit_amount=credit_amount,
                    voided_by=command.supervisor_id,
                    void_reason=command.reason,
                    occurred_at=now
                )

                # Dispatch sychronously in memory
                self.event_dispatcher.dispatch(event)

            self.db.commit()
            return updated_venta
        except Exception as e:
            self.db.rollback()
            raise e
