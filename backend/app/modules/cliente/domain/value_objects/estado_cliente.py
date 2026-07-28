from dataclasses import dataclass
from app.modules.cliente.domain.exceptions.cliente_invalido_exception import ClienteInvalidoException

@dataclass(frozen=True)
class EstadoCliente:
    valor: str

    def __post_init__(self) -> None:
        if not isinstance(self.valor, str):
            raise ClienteInvalidoException("El estado del cliente debe ser una cadena de texto.")
        
        normalized = self.valor.upper().strip()
        object.__setattr__(self, "valor", normalized)

        estados_validos = {"ACTIVO", "INACTIVO"}
        if self.valor not in estados_validos:
            raise ClienteInvalidoException(f"Estado de cliente '{self.valor}' invalido. Debe ser ACTIVO o INACTIVO.")

    @classmethod
    def activo(cls) -> "EstadoCliente":
        return cls("ACTIVO")

    @classmethod
    def inactivo(cls) -> "EstadoCliente":
        return cls("INACTIVO")

    @property
    def is_activo(self) -> bool:
        return self.valor == "ACTIVO"

    @property
    def is_inactivo(self) -> bool:
        return self.valor == "INACTIVO"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor == otro.upper().strip()
        if isinstance(otro, EstadoCliente):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return self.valor
