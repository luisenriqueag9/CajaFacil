from dataclasses import dataclass
from decimal import Decimal
from typing import Union
from app.modules.compra.domain.exceptions.compra_invalida_exception import CompraInvalidaException

@dataclass(frozen=True)
class Cantidad:
    valor: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.valor, Decimal):
            try:
                object.__setattr__(self, "valor", Decimal(str(self.valor)))
            except Exception:
                raise CompraInvalidaException(f"La cantidad recibida no es un numero decimal valido: {self.valor}")
        
        # Quantize to 4 decimal places for consistency
        object.__setattr__(self, "valor", self.valor.quantize(Decimal("0.0001")))

        if self.valor <= Decimal("0.0000"):
            raise CompraInvalidaException(
                f"La cantidad debe ser estrictamente mayor que cero. Valor recibido: {self.valor}"
            )

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, (Decimal, int, float)):
            try:
                dec_val = Decimal(str(otro)).quantize(Decimal("0.0001"))
                return self.valor == dec_val
            except Exception:
                return False
        if isinstance(otro, Cantidad):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return str(self.valor)
