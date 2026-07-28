from dataclasses import dataclass
from app.modules.compra.domain.exceptions.compra_invalida_exception import CompraInvalidaException

@dataclass(frozen=True)
class EstadoCompra:
    valor: str

    def __post_init__(self) -> None:
        if not isinstance(self.valor, str):
            raise CompraInvalidaException("El valor del estado debe ser una cadena de texto.")
        
        normalized = self.valor.upper().strip()
        object.__setattr__(self, "valor", normalized)

        estados_validos = {"BORRADOR", "REGISTRADA", "ANULADA"}
        if self.valor not in estados_validos:
            raise CompraInvalidaException(f"Estado de compra '{self.valor}' invalido. Debe ser BORRADOR, REGISTRADA o ANULADA.")

    @classmethod
    def borrador(cls) -> "EstadoCompra":
        return cls("BORRADOR")

    @classmethod
    def registrada(cls) -> "EstadoCompra":
        return cls("REGISTRADA")

    @classmethod
    def anulada(cls) -> "EstadoCompra":
        return cls("ANULADA")

    @property
    def is_borrador(self) -> bool:
        return self.valor == "BORRADOR"

    @property
    def is_registrada(self) -> bool:
        return self.valor == "REGISTRADA"

    @property
    def is_anulada(self) -> bool:
        return self.valor == "ANULADA"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor == otro.upper().strip()
        if isinstance(otro, EstadoCompra):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return self.valor
