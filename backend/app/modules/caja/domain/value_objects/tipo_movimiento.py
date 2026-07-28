from dataclasses import dataclass

@dataclass(frozen=True)
class TipoMovimiento:
    valor: str

    def __post_init__(self) -> None:
        normalized = self.valor.upper().strip()
        object.__setattr__(self, "valor", normalized)

        tipos_validos = {"INGRESO", "EGRESO"}
        if self.valor not in tipos_validos:
            raise ValueError(f"Tipo de movimiento '{self.valor}' invalido. Debe ser INGRESO o EGRESO.")

    @classmethod
    def ingreso(cls) -> "TipoMovimiento":
        return cls("INGRESO")

    @classmethod
    def egreso(cls) -> "TipoMovimiento":
        return cls("EGRESO")

    @property
    def is_ingreso(self) -> bool:
        return self.valor == "INGRESO"

    @property
    def is_egreso(self) -> bool:
        return self.valor == "EGRESO"

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, str):
            return self.valor == otro.upper().strip()
        if isinstance(otro, TipoMovimiento):
            return self.valor == otro.valor
        return False

    def __str__(self) -> str:
        return self.valor
