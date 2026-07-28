from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Union
from app.modules.caja.domain.exceptions.caja_exceptions import MontoInvalidoException

@dataclass(frozen=True)
class Dinero:
    monto: Decimal
    divisa: str = "NIO"

    def __post_init__(self) -> None:
        # Validate divisa
        if not isinstance(self.divisa, str) or len(self.divisa) != 3:
            raise ValueError("La divisa debe ser un codigo ISO de 3 caracteres.")
        
        normalized_divisa = self.divisa.upper().strip()
        object.__setattr__(self, "divisa", normalized_divisa)

        # Coerce and quantize monto to 4 decimal places
        if isinstance(self.monto, (int, float)):
            monto_dec = Decimal(str(self.monto))
        elif isinstance(self.monto, Decimal):
            monto_dec = self.monto
        else:
            raise ValueError("El monto debe ser un numero decimal, entero o flotante.")

        quantized_monto = monto_dec.quantize(Decimal("0.0000"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "monto", quantized_monto)

    @classmethod
    def cero(cls, divisa: str = "NIO") -> "Dinero":
        return cls(Decimal("0.0000"), divisa)

    def sumar(self, otro: "Dinero") -> "Dinero":
        if self.divisa != otro.divisa:
            raise ValueError(f"No se pueden sumar montos con diferentes divisas: {self.divisa} y {otro.divisa}.")
        return Dinero(self.monto + otro.monto, self.divisa)

    def restar(self, otro: "Dinero") -> "Dinero":
        if self.divisa != otro.divisa:
            raise ValueError(f"No se pueden restar montos con diferentes divisas: {self.divisa} y {otro.divisa}.")
        return Dinero(self.monto - otro.monto, self.divisa)

    def __add__(self, otro: "Dinero") -> "Dinero":
        return self.sumar(otro)

    def __sub__(self, otro: "Dinero") -> "Dinero":
        return self.restar(otro)

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, (int, float, Decimal)):
            return self.monto == Decimal(str(otro)).quantize(Decimal("0.0000"), rounding=ROUND_HALF_UP)
        if isinstance(otro, Dinero):
            return self.monto == otro.monto and self.divisa == otro.divisa
        return False

    def __lt__(self, otro: "Dinero") -> bool:
        if self.divisa != otro.divisa:
            raise ValueError("No se pueden comparar montos con diferentes divisas.")
        return self.monto < otro.monto

    def __le__(self, otro: "Dinero") -> bool:
        if self.divisa != otro.divisa:
            raise ValueError("No se pueden comparar montos con diferentes divisas.")
        return self.monto <= otro.monto

    def __gt__(self, otro: "Dinero") -> bool:
        if self.divisa != otro.divisa:
            raise ValueError("No se pueden comparar montos con diferentes divisas.")
        return self.monto > otro.monto

    def __ge__(self, otro: "Dinero") -> bool:
        if self.divisa != otro.divisa:
            raise ValueError("No se pueden comparar montos con diferentes divisas.")
        return self.monto >= otro.monto

    def __str__(self) -> str:
        return f"{self.monto} {self.divisa}"
