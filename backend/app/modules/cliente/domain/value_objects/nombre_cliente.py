from dataclasses import dataclass
from app.modules.cliente.domain.exceptions.cliente_invalido_exception import ClienteInvalidoException

@dataclass(frozen=True)
class NombreCliente:
    valor: str

    def __post_init__(self) -> None:
        if not self.valor or not isinstance(self.valor, str):
            raise ClienteInvalidoException("El nombre del cliente no puede estar vacio.")
        
        normalized = self.valor.strip()
        if len(normalized) < 2:
            raise ClienteInvalidoException("El nombre del cliente debe tener al menos 2 caracteres.")
        
        object.__setattr__(self, "valor", normalized)

    def __str__(self) -> str:
        return self.valor
