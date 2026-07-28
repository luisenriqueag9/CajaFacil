from dataclasses import dataclass
from decimal import Decimal
from typing import Union
from app.modules.compra.domain.exceptions.compra_invalida_exception import CompraInvalidaException
from app.modules.compra.domain.value_objects.cantidad import Cantidad

@dataclass(frozen=True)
class Dinero:
    monto: Decimal
    divisa: str = "NIO"

    def __post_init__(self) -> None:
        if not isinstance(self.monto, Decimal):
            try:
                object.__setattr__(self, "monto", Decimal(str(self.monto)))
            except Exception:
                raise CompraInvalidaException(f"El monto de dinero no es un numero decimal valido: {self.monto}")
        
        # Quantize to 4 decimal places for monetary integrity (Numeric(18,4))
        object.__setattr__(self, "monto", self.monto.quantize(Decimal("0.0001")))

        if self.monto < Decimal("0.0000"):
            raise CompraInvalidaException("El monto no puede ser negativo.")

        if not isinstance(self.divisa, str) or len(self.divisa) != 3:
            raise CompraInvalidaException("Divisa invalida. Debe ser codigo ISO de 3 letras.")
        
        object.__setattr__(self, "divisa", self.divisa.upper().strip())

    @classmethod
    def cero(cls, divisa: str = "NIO") -> "Dinero":
        return cls(Decimal("0.0000"), divisa)

    def sumar(self, otro: "Dinero") -> "Dinero":
        if self.divisa != otro.divisa:
            raise CompraInvalidaException(
                f"No se pueden sumar montos de distintas divisas: {self.divisa} y {otro.divisa}"
            )
        return Dinero(self.monto + otro.monto, self.divisa)

    def restar(self, otro: "Dinero") -> "Dinero":
        if self.divisa != otro.divisa:
            raise CompraInvalidaException(
                f"No se pueden restar montos de distintas divisas: {self.divisa} y {otro.divisa}"
            )
        return Dinero(self.monto - otro.monto, self.divisa)

    def multiplicar(self, factor: Union[Decimal, Cantidad, int, float]) -> "Dinero":
        if isinstance(factor, Cantidad):
            factor_val = factor.valor
        elif isinstance(factor, Decimal):
            factor_val = factor
        else:
            try:
                factor_val = Decimal(str(factor))
            except Exception:
                raise CompraInvalidaException(f"Factor de multiplicacion invalido: {factor}")
        
        return Dinero(self.monto * factor_val, self.divisa)

    def __add__(self, otro: "Dinero") -> "Dinero":
        return self.sumar(otro)

    def __sub__(self, otro: "Dinero") -> "Dinero":
        return self.restar(otro)

    def __mul__(self, factor: Union[Decimal, Cantidad, int, float]) -> "Dinero":
        return self.multiplicar(factor)

    def __rmul__(self, factor: Union[Decimal, Cantidad, int, float]) -> "Dinero":
        return self.multiplicar(factor)

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, (Decimal, int, float)):
            try:
                dec_val = Decimal(str(otro)).quantize(Decimal("0.0001"))
                return self.monto == dec_val
            except Exception:
                return False
        if isinstance(otro, Dinero):
            return self.monto == otro.monto and self.divisa == otro.divisa
        return False

    def __str__(self) -> str:
        return f"{self.monto} {self.divisa}"
