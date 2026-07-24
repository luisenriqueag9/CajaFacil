import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario, AjusteInventario
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.domain.exceptions import ProductoNoManejaInventarioException
from app.modules.inventario.domain.events.inventario_events import InventarioActualizado, AjusteInventarioRegistrado
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class RegistrarAjusteCommand:
    company_id: uuid.UUID
    product_id: uuid.UUID
    physical_quantity: Decimal
    supervisor_id: uuid.UUID
    notes: str | None = None

class RegistrarAjusteUseCase:
    """
    Application Use Case to adjust logical stock levels to match physical audit counts.
    Creates a corrective ENTRADA or SALIDA movement and overwrites fast stock balance (ExistenciaProducto).
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

    def execute(self, command: RegistrarAjusteCommand) -> MovimientoInventario:
        # 1. Basic validation
        if command.physical_quantity < Decimal("0.0000"):
            raise ValidationException("La cantidad física de inventario no puede ser negativa.")

        # 2. Product validation
        product_details = self.product_lookup.get_details(command.company_id, command.product_id)
        if not product_details.exists:
            raise ValidationException(f"El producto '{command.product_id}' no existe en esta empresa.")
        if not product_details.active:
            raise ValidationException(f"El producto '{command.product_id}' está inactivo.")
        if not product_details.controls_stock:
            raise ProductoNoManejaInventarioException(command.product_id)

        # 3. Retrieve ExistenciaProducto to find system quantity (logical stock)
        existencia = self.existencia_repository.get_by_product_id(command.company_id, command.product_id)
        if existencia is None:
            existencia = ExistenciaProducto(
                id=uuid.uuid4(),
                company_id=command.company_id,
                product_id=command.product_id,
                stock=Decimal("0.0000")
            )

        system_quantity = existencia.stock

        # 4. Calculate difference
        difference = command.physical_quantity - system_quantity
        if difference == Decimal("0.0000"):
            raise ValidationException(
                "La cantidad física coincide exactamente con el saldo lógico del sistema; no se requiere ajuste."
            )

        # 5. Determine movement direction and quantity
        if difference > Decimal("0.0000"):
            mov_type = "ENTRADA"
            qty = difference
        else:
            mov_type = "SALIDA"
            qty = abs(difference)

        # 6. Apply adjustment to stock balance
        existencia.ajustar(command.physical_quantity)

        # 7. Construct domain entities
        now = datetime.now(timezone.utc)
        movimiento_id = uuid.uuid4()
        ajuste_id = uuid.uuid4()

        ajuste = AjusteInventario(
            id=ajuste_id,
            physical_quantity=command.physical_quantity,
            system_quantity=system_quantity,
            difference=difference
        )

        movimiento = MovimientoInventario(
            id=movimiento_id,
            company_id=command.company_id,
            product_id=command.product_id,
            type=mov_type,
            concept="AJUSTE",
            quantity=qty,
            origin_document_id=None,
            created_at=now,
            created_by=command.supervisor_id,
            notes=command.notes or f"Ajuste correctivo de inventario físico. Diferencia: {difference}",
            ajuste=ajuste
        )

        # 8. Execute transaction (Unit of Work)
        try:
            with self.db.begin_nested():
                saved_mov = self.repository.save(movimiento)
                self.existencia_repository.save(existencia)
                
                # Dispatch events synchronously
                change_qty = qty if mov_type == "ENTRADA" else -qty
                
                ev_update = InventarioActualizado(
                    product_id=saved_mov.product_id,
                    company_id=saved_mov.company_id,
                    quantity_change=change_qty,
                    new_balance=existencia.stock,
                    type=mov_type,
                    concept="AJUSTE",
                    occurred_at=saved_mov.created_at
                )
                
                ev_ajuste = AjusteInventarioRegistrado(
                    ajuste_id=ajuste_id,
                    movimiento_id=movimiento_id,
                    product_id=saved_mov.product_id,
                    physical_quantity=command.physical_quantity,
                    system_quantity=system_quantity,
                    difference=difference,
                    occurred_at=saved_mov.created_at
                )
                
                self.event_dispatcher.dispatch(ev_update)
                self.event_dispatcher.dispatch(ev_ajuste)
            self.db.commit()
            return saved_mov
        except Exception as e:
            self.db.rollback()
            raise e
