from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from typing import Union
from app.modules.compra.domain.exceptions.compra_invalida_exception import CompraInvalidaException
from app.modules.compra.domain.value_objects.cantidad import Cantidad
from app.modules.compra.domain.value_objects.dinero import Dinero

@dataclass
class DetalleCompra:
    id: UUID
    purchase_id: UUID
    product_id: UUID
    quantity: Union[Cantidad, Decimal, int, float]
    unit_cost: Union[Dinero, Decimal, int, float]

    def __post_init__(self) -> None:
        # Coerce raw values to their respective Value Objects for DDD integrity
        if not isinstance(self.quantity, Cantidad):
            self.quantity = Cantidad(self.quantity)
        if not isinstance(self.unit_cost, Dinero):
            self.unit_cost = Dinero(self.unit_cost)
        
        self.validate()

    def validate(self) -> None:
        if not self.product_id:
            raise CompraInvalidaException("El producto es obligatorio en cada linea de detalle.")
        # Quantity and unit_cost validate their own business constraints (strictly positive / non-negative)

    @property
    def line_total(self) -> Dinero:
        return self.unit_cost.multiplicar(self.quantity)
