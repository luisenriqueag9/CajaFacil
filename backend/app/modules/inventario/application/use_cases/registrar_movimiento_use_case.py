import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.domain.exceptions import (
    StockInsuficienteException,
    ProductoNoManejaInventarioException
)
from app.modules.inventario.domain.events.inventario_events import InventarioActualizado
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class RegistrarMovimientoCommand:
    company_id: UUID
    product_id: UUID
    type: str  # ENTRADA, SALIDA
    concept: str
    quantity: Decimal
    created_by: UUID
    origin_document_id: UUID | None = None
    notes: str | None = None

class RegistrarMovimientoUseCase:
    """
    Application Use Case to record inventory movements (additions or subtractions).
    Coordinates SQLite transactional boundary and verifies inventory constraints.
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

    def execute(self, command: RegistrarMovimientoCommand) -> MovimientoInventario:
        # 1. Query product catalog specs through the lookup port
        product_details = self.product_lookup.get_details(command.company_id, command.product_id)
        if not product_details.exists:
            raise ValidationException(f"El producto '{command.product_id}' no existe en esta empresa.")
        if not product_details.active:
            raise ValidationException(f"El producto '{command.product_id}' está inactivo.")
        if not product_details.controls_stock:
            raise ProductoNoManejaInventarioException(command.product_id)

        # 2. Derive stock balance by aggregating existing movements (Kardex logic)
        movements = self.repository.get_by_product_id(command.company_id, command.product_id)
        current_stock = Decimal("0.0000")
        for m in movements:
            if m.type == "ENTRADA":
                current_stock += m.quantity
            elif m.type == "SALIDA":
                current_stock -= m.quantity

        # 3. Check for stock shortage if negative stock is prohibited
        if command.type == "SALIDA" and not product_details.allows_negative:
            if current_stock - command.quantity < Decimal("0.0000"):
                raise StockInsuficienteException(command.product_id, float(current_stock), float(command.quantity))

        # 4. Construct domain aggregate root (runs entity-level validation)
        now = datetime.now(timezone.utc)
        movimiento = MovimientoInventario(
            id=uuid.uuid4(),
            company_id=command.company_id,
            product_id=command.product_id,
            type=command.type,
            concept=command.concept,
            quantity=command.quantity,
            origin_document_id=command.origin_document_id,
            created_at=now,
            created_by=command.created_by,
            notes=command.notes
        )

        # 5. Coordinate Unit of Work Transaction
        try:
            with self.db.begin_nested():
                saved_mov = self.repository.save(movimiento)
                
                # Sychronously dispatch consistency events
                change = command.quantity if command.type == "ENTRADA" else -command.quantity
                new_balance = current_stock + change
                
                event = InventarioActualizado(
                    product_id=saved_mov.product_id,
                    company_id=saved_mov.company_id,
                    quantity_change=change,
                    new_balance=new_balance,
                    type=saved_mov.type,
                    concept=saved_mov.concept,
                    occurred_at=saved_mov.created_at
                )
                self.event_dispatcher.dispatch(event)
            self.db.commit()
            return saved_mov
        except Exception as e:
            self.db.rollback()
            raise e
