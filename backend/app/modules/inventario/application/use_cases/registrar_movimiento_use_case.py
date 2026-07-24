import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.domain.exceptions import ProductoNoManejaInventarioException
from app.modules.inventario.domain.events.inventario_events import InventarioActualizado
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class RegistrarMovimientoCommand:
    company_id: uuid.UUID
    product_id: uuid.UUID
    type: str  # ENTRADA, SALIDA
    concept: str
    quantity: Decimal
    created_by: uuid.UUID
    origin_document_id: uuid.UUID | None = None
    notes: str | None = None

class RegistrarMovimientoUseCase:
    """
    Application Use Case to record inventory movements (additions or subtractions).
    Coordinates SQLite transactional boundary and updates ExistenciaProducto fast balance.
    """
    def __init__(
        self,
        repository: MovimientoInventarioRepository,
        existencia_repository: ExistenciaRepository,
        db: Session,
        event_dispatcher: EventDispatcher,
        product_lookup: ProductLookup
    ):
        self.repository = repository
        self.existencia_repository = existencia_repository
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

        # 2. Retrieve fast stock balance projection (ExistenciaProducto)
        existencia = self.existencia_repository.get_by_product_id(command.company_id, command.product_id)
        if existencia is None:
            existencia = ExistenciaProducto(
                id=uuid.uuid4(),
                company_id=command.company_id,
                product_id=command.product_id,
                stock=Decimal("0.0000")
            )

        # 3. Apply domain invariants and update stock balance
        if command.type == "ENTRADA":
            existencia.incrementar(command.quantity)
        elif command.type == "SALIDA":
            existencia.decrementar(command.quantity, allows_negative=product_details.allows_negative)
        else:
            raise ValueError(f"Tipo de movimiento inválido: {command.type}")

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
                self.existencia_repository.save(existencia)
                
                # Synchronously dispatch consistency events
                change = command.quantity if command.type == "ENTRADA" else -command.quantity
                
                event = InventarioActualizado(
                    product_id=saved_mov.product_id,
                    company_id=saved_mov.company_id,
                    quantity_change=change,
                    new_balance=existencia.stock,
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
