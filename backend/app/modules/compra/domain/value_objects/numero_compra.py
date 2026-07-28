from dataclasses import dataclass
from app.modules.compra.domain.exceptions.compra_invalida_exception import CompraInvalidaException

@dataclass(frozen=True)
class NumeroCompra:
    valor: str

    def __post_init__(self) -> None:
        if not isinstance(self.valor, str):
            raise CompraInvalidaException("El numero de compra/factura debe ser una cadena de texto.")
        
        normalized = self.valor.strip()
        object.__setattr__(self, "valor", normalized)

        if not normalized:
            raise CompraInvalidaException("El numero de factura no puede estar vacio.")

    def lower(self) -> str:
        return self.valor.lower()

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor.lower() == otro.strip().lower()
        if isinstance(otro, NumeroCompra):
            return self.valor.lower() == otro.valor.lower()
        return False

    def __str__(self) -> str:
        return self.valor
