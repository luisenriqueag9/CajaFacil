from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.modules.supplier.domain.exceptions.invalid_supplier_exception import InvalidSupplierException

@dataclass
class Supplier:
    id: UUID
    company_id: UUID
    name: str
    tax_id: str | None
    contact_name: str | None
    phone: str | None
    email: str | None
    status: str
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
        tax_id: str | None, 
        contact_name: str | None, 
        phone: str | None, 
        email: str | None, 
        created_at: datetime, 
        updated_at: datetime
    ) -> "Supplier":
        """
        Factory method to register a new active supplier.
        """
        return cls(
            id=id,
            company_id=company_id,
            name=name,
            tax_id=tax_id,
            contact_name=contact_name,
            phone=phone,
            email=email,
            status="ACTIVO",
            created_at=created_at,
            updated_at=updated_at,
        )

    def update_profile(
        self, 
        name: str, 
        tax_id: str | None, 
        contact_name: str | None, 
        phone: str | None, 
        email: str | None
    ) -> None:
        """
        Updates the supplier contact details and re-validates.
        """
        self.name = name
        self.tax_id = tax_id
        self.contact_name = contact_name
        self.phone = phone
        self.email = email
        self.validate()

    def deactivate(self) -> None:
        self.status = "INACTIVO"
        self.validate()

    def activate(self) -> None:
        self.status = "ACTIVO"
        self.validate()

    def validate(self) -> None:
        if not self.company_id:
            raise InvalidSupplierException("El proveedor debe pertenecer a una empresa (company_id es requerido).")
        if not self.name or not self.name.strip():
            raise InvalidSupplierException("El nombre del proveedor no puede estar vacío.")
        
        # If tax_id is provided, verify it is not blank
        if self.tax_id is not None and not self.tax_id.strip():
            raise InvalidSupplierException("La identificación tributaria no puede estar vacía si se proporciona.")
            
        valid_statuses = {"ACTIVO", "INACTIVO"}
        if self.status not in valid_statuses:
            raise InvalidSupplierException(
                f"Estado '{self.status}' no permitido. Estados válidos: ACTIVO, INACTIVO"
            )
