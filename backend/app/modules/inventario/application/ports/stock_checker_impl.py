from uuid import UUID
from decimal import Decimal
from app.modules.inventario.application.ports.stock_checker import StockCheckerPort
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.application.ports.product_lookup import ProductLookup
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto

class StockCheckerImpl(StockCheckerPort):
    """
    Concrete implementation of StockCheckerPort that uses ExistenciaRepository
    and ProductLookup to verify stock availability.
    """
    def __init__(self, existencia_repository: ExistenciaRepository, product_lookup: ProductLookup):
        self.existencia_repository = existencia_repository
        self.product_lookup = product_lookup

    def has_sufficient_stock(self, company_id: UUID, product_id: UUID, quantity: Decimal) -> bool:
        product_details = self.product_lookup.get_details(company_id, product_id)
        if not product_details.exists or not product_details.active:
            return False
        
        if not product_details.controls_stock:
            return True

        if product_details.allows_negative:
            return True

        existencia = self.existencia_repository.get_by_product_id(company_id, product_id)
        current_stock = existencia.stock if existencia else Decimal("0.0000")

        return (current_stock - quantity) >= Decimal("0.0000")
