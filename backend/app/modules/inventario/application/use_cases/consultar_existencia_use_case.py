import uuid
from uuid import UUID
from decimal import Decimal
from app.common.exceptions import ValidationException
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.domain.exceptions import ProductoNoManejaInventarioException

class ConsultarExistenciaUseCase:
    """
    Application Use Case to query the fast available stock of a product.
    Queries the ExistenciaProducto Aggregate.
    """
    def __init__(self, repository: ExistenciaRepository, product_lookup: ProductLookup):
        self.repository = repository
        self.product_lookup = product_lookup

    def execute(self, company_id: UUID, product_id: UUID) -> ExistenciaProducto:
        # Validate catalog details
        product_details = self.product_lookup.get_details(company_id, product_id)
        if not product_details.exists:
            raise ValidationException(f"El producto '{product_id}' no existe en esta empresa.")
        if not product_details.controls_stock:
            raise ProductoNoManejaInventarioException(product_id)

        existencia = self.repository.get_by_product_id(company_id, product_id)
        if existencia is None:
            # Initialize to 0 if not exists in DB yet
            existencia = ExistenciaProducto(
                id=uuid.uuid4(),
                company_id=company_id,
                product_id=product_id,
                stock=Decimal("0.0000")
            )
            # Persist the newly initialized stock
            self.repository.save(existencia)

        return existencia
