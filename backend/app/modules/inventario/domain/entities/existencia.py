from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from app.modules.inventario.domain.exceptions import StockInsuficienteException

@dataclass
class ExistenciaProducto:
    id: UUID
    company_id: UUID
    product_id: UUID
    stock: Decimal = Decimal("0.0000")

    def incrementar(self, quantity: Decimal) -> None:
        if quantity <= Decimal("0.0000"):
            raise ValueError("La cantidad a incrementar debe ser mayor que cero.")
        self.stock += quantity

    def decrementar(self, quantity: Decimal, allows_negative: bool = False) -> None:
        if quantity <= Decimal("0.0000"):
            raise ValueError("La cantidad a decrementar debe ser mayor que cero.")
        
        if not allows_negative and (self.stock - quantity) < Decimal("0.0000"):
            raise StockInsuficienteException(
                product_id=self.product_id,
                current_stock=float(self.stock),
                requested=float(quantity)
            )
        self.stock -= quantity

    def ajustar(self, physical_quantity: Decimal) -> None:
        self.stock = physical_quantity
