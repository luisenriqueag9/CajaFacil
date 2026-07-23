import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario, Merma
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.domain.exceptions import (
    StockInsuficienteException,
    ProductoNoManejaInventarioException
)
from app.modules.inventario.domain.events.inventario_events import InventarioActualizado, MermaRegistrada
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class RegistrarMermaCommand:
    company_id: UUID
    product_id: UUID
    quantity: Decimal
    reason: str  # ROTURA, VENCIMIENTO, ROBO, OTRO
    created_by: UUID
    description: str | None = None

class RegistrarMermaUseCase:
    """
    Application Use Case to record inventory waste/mermas.
    Reduces physical stock and stores justification.
    """
    def __init__(
        self,
        repository: MovimientoInventarioRepository,
        db: Session,
        event_dispatcher: EventDispatcher,
        product_lookup: ProductLookup
    ):
        self.repository = repository
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.product_lookup = product_lookup

    def execute(self, command: RegistrarMermaCommand) -> MovimientoInventario:
        # 1. Product details validation
        product_details = self.product_lookup.get_details(command.company_id, command.product_id)
        if not product_details.exists:
            raise ValidationException(f"El producto '{command.product_id}' no existe en esta empresa.")
        if not product_details.active:
            raise ValidationException(f"El producto '{command.product_id}' está inactivo.")
        if not product_details.controls_stock:
            raise ProductoNoManejaInventarioException(command.product_id)

        # 2. Derive stock balance
        movements = self.repository.get_by_product_id(command.company_id, command.product_id)
        current_stock = Decimal("0.0000")
        for m in movements:
            if m.type == "ENTRADA":
                current_stock += m.quantity
            elif m.type == "SALIDA":
                current_stock -= m.quantity

        # 3. Check for stock shortage
        if not product_details.allows_negative:
            if current_stock - command.quantity < Decimal("0.0000"):
                raise StockInsuficienteException(command.product_id, float(current_stock), float(command.quantity))

        # 4. Construct domain entities
        now = datetime.now(timezone.utc)
        movimiento_id = uuid.uuid4()
        merma_id = uuid.uuid4()

        merma = Merma(
            id=merma_id,
            reason=command.reason,
            description=command.description
        )

        movimiento = MovimientoInventario(
            id=movimiento_id,
            company_id=command.company_id,
            product_id=command.product_id,
            type="SALIDA",
            concept="MERMA",
            quantity=command.quantity,
            origin_document_id=None,
            created_at=now,
            created_by=command.created_by,
            notes=f"Registro de merma por: {command.reason}",
            merma=merma
        )

        # 5. Execute transaction (Unit of Work)
        try:
            with self.db.begin_nested():
                saved_mov = self.repository.save(movimiento)
                
                # Dispatch events sychronously
                new_balance = current_stock - command.quantity
                
                ev_update = InventarioActualizado(
                    product_id=saved_mov.product_id,
                    company_id=saved_mov.company_id,
                    quantity_change=-command.quantity,
                    new_balance=new_balance,
                    type="SALIDA",
                    concept="MERMA",
                    occurred_at=saved_mov.created_at
                )
                
                ev_merma = MermaRegistrada(
                    merma_id=merma_id,
                    movimiento_id=movimiento_id,
                    product_id=saved_mov.product_id,
                    quantity=command.quantity,
                    reason=command.reason,
                    occurred_at=saved_mov.created_at
                )
                
                self.event_dispatcher.dispatch(ev_update)
                self.event_dispatcher.dispatch(ev_merma)
            self.db.commit()
            return saved_mov
        except Exception as e:
            self.db.rollback()
            raise e
