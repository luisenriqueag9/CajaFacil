import uuid
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session

from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.domain.exceptions import ProductoNoManejaInventarioException

class RecalcularExistenciaDesdeKardexUseCase:
    """
    Administrative fallback Use Case to reconstruct the fast stock balance (ExistenciaProducto)
    by summing all historical movement transactions (MovimientoInventario) from the Kardex.
    """
    def __init__(
        self,
        existencia_repository: ExistenciaRepository,
        movimiento_repository: MovimientoInventarioRepository,
        product_lookup: ProductLookup,
        db: Session
    ):
        self.existencia_repository = existencia_repository
        self.movimiento_repository = movimiento_repository
        self.product_lookup = product_lookup
        self.db = db

    def execute(self, company_id: UUID, product_id: UUID) -> ExistenciaProducto:
        # Validate catalog details
        product_details = self.product_lookup.get_details(company_id, product_id)
        if not product_details.exists:
            raise ValidationException(f"El producto '{product_id}' no existe en esta empresa.")
        if not product_details.controls_stock:
            raise ProductoNoManejaInventarioException(product_id)

        # 1. Sum up all movements
        movements = self.movimiento_repository.get_by_product_id(company_id, product_id)
        computed_stock = Decimal("0.0000")
        for m in movements:
            if m.type == "ENTRADA":
                computed_stock += m.quantity
            elif m.type == "SALIDA":
                computed_stock -= m.quantity

        # 2. Retrieve or initialize ExistenciaProducto
        existencia = self.existencia_repository.get_by_product_id(company_id, product_id)
        if existencia is None:
            existencia = ExistenciaProducto(
                id=uuid.uuid4(),
                company_id=company_id,
                product_id=product_id,
                stock=Decimal("0.0000")
            )

        # 3. Adjust and save in transaction
        try:
            with self.db.begin_nested():
                existencia.ajustar(computed_stock)
                saved_existencia = self.existencia_repository.save(existencia)
            self.db.commit()
            return saved_existencia
        except Exception as e:
            self.db.rollback()
            raise e
