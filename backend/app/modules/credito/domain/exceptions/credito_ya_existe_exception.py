from uuid import UUID
from fastapi import status
from app.common.exceptions import ValidationException

class CreditoYaExisteException(ValidationException):
    """
    Excepcion lanzada cuando ya existe una cuenta de credito para el cliente.
    """
    def __init__(self, client_id: UUID, company_id: UUID):
        super().__init__(
            message=f"El cliente con ID '{client_id}' ya posee una cuenta de credito registrada para la empresa '{company_id}'.",
            code="CREDITO_YA_EXISTE",
            details={
                "client_id": str(client_id),
                "company_id": str(company_id)
            }
        )
        self.status_code = status.HTTP_409_CONFLICT
