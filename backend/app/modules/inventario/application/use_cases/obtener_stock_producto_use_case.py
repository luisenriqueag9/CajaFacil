from uuid import UUID
from decimal import Decimal
from app.common.exceptions import ValidationException
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.domain.exceptions import ProductoNoManejaInventarioException
from app.modules.inventario.application.ports.product_lookup import ProductLookup

class ObtenerStockProductoUseCase:
    """
    Application Use Case to query the current computed balance of stock for a product.
    """
    def __init__(self, repository: MovimientoInventarioRepository, product_lookup: ProductLookup):
        self.repository = repository
        self.product_lookup = product_lookup

    def execute(self, company_id: UUID, product_id: UUID) -> Decimal:
        # Validate catalog specifications first
        product_details = self.product_lookup.get_details(company_id, product_id)
        if not product_details.exists:
            raise ValidationException(f"El producto '{product_id}' no existe en esta empresa.")
        if not product_details.controls_stock:
            raise ProductoNoManejaInventarioException(product_id)

        # Retrieve and calculate balance
        movements = self.repository.get_by_product_id(company_id, product_id)
        stock = Decimal("0.0000")
        for m in movements:
            if m.type == "ENTRADA":
                stock += m.quantity
            elif m.type == "SALIDA":
                stock -= m.quantity
        return stock
