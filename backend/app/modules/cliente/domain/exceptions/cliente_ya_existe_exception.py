from uuid import UUID
from fastapi import status
from app.common.exceptions import ValidationException

class ClienteYaExisteException(ValidationException):
    """
    Excepcion lanzada cuando ya existe un cliente con el mismo tax_id en la empresa.
    """
    def __init__(self, tax_id: str, company_id: UUID):
        super().__init__(
            message=f"Ya existe un cliente con el identificador tributario '{tax_id}' para la empresa '{company_id}'.",
            code="CLIENTE_YA_EXISTE",
            details={
                "tax_id": tax_id,
                "company_id": str(company_id)
            }
        )
        self.status_code = status.HTTP_409_CONFLICT
