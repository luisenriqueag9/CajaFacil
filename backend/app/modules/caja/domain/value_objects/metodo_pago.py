from dataclasses import dataclass

@dataclass(frozen=True)
class MetodoPago:
    valor: str

    def __post_init__(self) -> None:
        normalized = self.valor.upper().strip()
        object.__setattr__(self, "valor", normalized)

        metodos_validos = {"EFECTIVO", "TARJETA", "TRANSFERENCIA", "CREDITO"}
        if self.valor not in metodos_validos:
            raise ValueError(f"Metodo de pago '{self.valor}' invalido. Debe ser EFECTIVO, TARJETA, TRANSFERENCIA o CREDITO.")

    @classmethod
    def efectivo(cls) -> "MetodoPago":
        return cls("EFECTIVO")

    @classmethod
    def tarjeta(cls) -> "MetodoPago":
        return cls("TARJETA")

    @classmethod
    def transferencia(cls) -> "MetodoPago":
        return cls("TRANSFERENCIA")

    @classmethod
    def credito(cls) -> "MetodoPago":
        return cls("CREDITO")

    @property
    def is_efectivo(self) -> bool:
        return self.valor == "EFECTIVO"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor == otro.upper().strip()
        if isinstance(otro, MetodoPago):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return self.valor
