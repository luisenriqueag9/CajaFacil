from dataclasses import dataclass
from app.modules.credito.domain.exceptions.credito_invalido_exception import CreditoInvalidoException

@dataclass(frozen=True)
class EstadoCredito:
    valor: str

    def __post_init__(self) -> None:
        if not isinstance(self.valor, str):
            raise CreditoInvalidoException("El valor del estado debe ser una cadena de texto.")
        
        normalized = self.valor.upper().strip()
        object.__setattr__(self, "valor", normalized)

        estados_validos = {"ACTIVO", "SUSPENDIDO"}
        if self.valor not in estados_validos:
            raise CreditoInvalidoException(f"Estado de credito '{self.valor}' invalido. Debe ser ACTIVO o SUSPENDIDO.")

    @classmethod
    def activo(cls) -> "EstadoCredito":
        return cls("ACTIVO")

    @classmethod
    def suspendido(cls) -> "EstadoCredito":
        return cls("SUSPENDIDO")

    @property
    def is_activo(self) -> bool:
        return self.valor == "ACTIVO"

    @property
    def is_suspendido(self) -> bool:
        return self.valor == "SUSPENDIDO"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor == otro.upper().strip()
        if isinstance(otro, EstadoCredito):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return self.valor
