from dataclasses import dataclass
from uuid import UUID
from app.modules.purchase.domain.exceptions.invalid_purchase_exception import InvalidPurchaseException

@dataclass
class PurchaseDetail:
    id: UUID
    purchase_id: UUID
    product_id: UUID
    quantity: float
    unit_cost: float

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.product_id:
            raise InvalidPurchaseException("El producto es obligatorio en cada línea de detalle.")
        if self.quantity <= 0:
            raise InvalidPurchaseException(
                f"La cantidad debe ser estrictamente mayor que cero. Valor recibido: {self.quantity}"
            )
        if self.unit_cost < 0:
            raise InvalidPurchaseException(
                f"El costo unitario no puede ser negativo. Valor recibido: {self.unit_cost}"
            )

    @property
    def line_total(self) -> float:
        return self.quantity * self.unit_cost
