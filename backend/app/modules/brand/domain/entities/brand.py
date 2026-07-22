from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.modules.brand.domain.exceptions.invalid_brand_exception import InvalidBrandException

@dataclass
class Brand:
    id: UUID
    company_id: UUID
    name: str
    status: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        self.validate()

    def rename(self, new_name: str) -> None:
        """
        Renames the brand revalidating invariants.
        """
        self.name = new_name
        self.validate()

    def deactivate(self) -> None:
        """
        Deactivates the brand (sets status to INACTIVO).
        """
        self.status = "INACTIVO"
        self.validate()

    def activate(self) -> None:
        """
        Activates the brand (sets status to ACTIVO).
        """
        self.status = "ACTIVO"
        self.validate()

    def validate(self) -> None:
        """
        Protects the brand's invariants.
        """
        if not self.company_id:
            raise InvalidBrandException("La marca debe pertenecer a una empresa (company_id es requerido).")
        if not self.name or not self.name.strip():
            raise InvalidBrandException("El nombre de la marca no puede estar vacío.")
        if len(self.name) > 100:
            raise InvalidBrandException("El nombre de la marca no puede superar los 100 caracteres.")
        
        valid_statuses = {"ACTIVO", "INACTIVO"}
        if self.status not in valid_statuses:
            raise InvalidBrandException(
                f"Estado '{self.status}' no permitido. Estados válidos: ACTIVO, INACTIVO"
            )
