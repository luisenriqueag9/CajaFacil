from uuid import UUID
from app.common.exceptions import NotFoundException

class CreditoNoEncontradoException(NotFoundException):
    """
    Excepcion lanzada cuando la cuenta de credito no existe.
    """
    def __init__(self, credit_id: UUID):
        super().__init__(
            message=f"La cuenta de credito con ID '{credit_id}' no fue encontrada.",
            code="CREDITO_NO_ENCONTRADO",
            details={
                "credit_id": str(credit_id)
            }
        )
