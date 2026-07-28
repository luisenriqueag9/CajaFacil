import re
from dataclasses import dataclass
from app.modules.cliente.domain.exceptions.cliente_invalido_exception import ClienteInvalidoException

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

@dataclass(frozen=True)
class EmailCliente:
    valor: str | None

    def __post_init__(self) -> None:
        if self.valor is None:
            return
            
        if not isinstance(self.valor, str):
            raise ClienteInvalidoException("El email debe ser una cadena de texto.")

        normalized = self.valor.strip().lower()
        if normalized == "":
            object.__setattr__(self, "valor", None)
            return

        if not EMAIL_REGEX.match(normalized):
            raise ClienteInvalidoException(f"El email '{self.valor}' no tiene un formato valido.")

        object.__setattr__(self, "valor", normalized)

    def __str__(self) -> str:
        return self.valor or ""
