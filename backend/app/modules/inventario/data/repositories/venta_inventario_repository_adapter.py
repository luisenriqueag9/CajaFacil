import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session

from app.modules.venta.application.ports.movimiento_inventario_repository import MovimientoInventarioRepository
from app.modules.inventario.data.repositories.movimiento_repository_impl import MovimientoInventarioRepositoryImpl
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario

class VentaInventoryRepositoryAdapter(MovimientoInventarioRepository):
    """
    Adapter implementation of Ventas's MovimientoInventarioRepository port.
    Resides in Inventario module and communicates with Inventario domain aggregates and repositories.
    """
    def __init__(self, db: Session):
        self.db = db

    def registrar_movimiento(
        self,
        company_id: uuid.UUID,
        product_id: uuid.UUID,
        quantity: Decimal,
        tipo: str,
        concept: str,
        reference_id: uuid.UUID
    ) -> None:
        repo = MovimientoInventarioRepositoryImpl(self.db)
        
        mov = MovimientoInventario(
            id=uuid.uuid4(),
            company_id=company_id,
            product_id=product_id,
            type=tipo,
            concept=concept,
            quantity=quantity,
            origin_document_id=reference_id,
            created_by=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            notes="Registrado automaticamente por venta",
            created_at=datetime.now(timezone.utc)
        )
        repo.save(mov)
