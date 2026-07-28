from dataclasses import dataclass
from app.modules.caja.domain.exceptions.caja_exceptions import CajaCerradaException

@dataclass(frozen=True)
class EstadoSesion:
    valor: str

    def __post_init__(self) -> None:
        normalized = self.valor.upper().strip()
        object.__setattr__(self, "valor", normalized)

        estados_validos = {"ABIERTA", "CERRADA"}
        if self.valor not in estados_validos:
            raise ValueError(f"Estado de sesion '{self.valor}' invalido. Debe ser ABIERTA o CERRADA.")

    @classmethod
    def abierta(cls) -> "EstadoSesion":
        return cls("ABIERTA")

    @classmethod
    def cerrada(cls) -> "EstadoSesion":
        return cls("CERRADA")

    @property
    def is_abierta(self) -> bool:
        return self.valor == "ABIERTA"

    @property
    def is_cerrada(self) -> bool:
        return self.valor == "CERRADA"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor == otro.upper().strip()
        if isinstance(otro, EstadoSesion):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return self.valor
