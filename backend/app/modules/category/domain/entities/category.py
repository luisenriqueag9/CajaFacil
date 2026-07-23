from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.modules.category.domain.exceptions.invalid_category_exception import InvalidCategoryException

@dataclass
class Category:
    id: UUID
    company_id: UUID
    name: str
    status: str
    protected: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        self.validate()

    @classmethod
    def register(
        cls, 
        id: UUID, 
        company_id: UUID, 
        name: str, 
        created_at: datetime, 
        updated_at: datetime
    ) -> "Category":
        """
        Factory method to register a merchant-owned category.
        """
        return cls(
            id=id,
            company_id=company_id,
            name=name,
            status="ACTIVO",
            protected=False,
            created_at=created_at,
            updated_at=updated_at,
        )

    @classmethod
    def initialize_default(
        cls, 
        id: UUID, 
        company_id: UUID, 
        name: str, 
        created_at: datetime, 
        updated_at: datetime
    ) -> "Category":
        """
        Factory method to initialize a protected system category (e.g. 'Sin Clasificar').
        """
        return cls(
            id=id,
            company_id=company_id,
            name=name,
            status="ACTIVO",
            protected=True,
            created_at=created_at,
            updated_at=updated_at,
        )

    def rename(self, new_name: str) -> None:
        if self.protected:
            raise InvalidCategoryException("No se puede renombrar una categoría protegida del sistema.")
        self.name = new_name
        self.validate()

    def deactivate(self) -> None:
        if self.protected:
            raise InvalidCategoryException("No se puede desactivar una categoría protegida del sistema.")
        self.status = "INACTIVO"
        self.validate()

    def activate(self) -> None:
        self.status = "ACTIVO"
        self.validate()

    def validate(self) -> None:
        if not self.company_id:
            raise InvalidCategoryException("La categoría debe pertenecer a una empresa (company_id es requerido).")
        if not self.name or not self.name.strip():
            raise InvalidCategoryException("El nombre de la categoría no puede estar vacío.")
        
        valid_statuses = {"ACTIVO", "INACTIVO"}
        if self.status not in valid_statuses:
            raise InvalidCategoryException(
                f"Estado '{self.status}' no permitido. Estados válidos: ACTIVO, INACTIVO"
            )
