from uuid import UUID
from app.common.exceptions import NotFoundException

class ClienteNoEncontradoException(NotFoundException):
    """
    Excepcion lanzada cuando el cliente solicitado no existe.
    """
    def __init__(self, client_id: UUID):
        super().__init__(
            message=f"El cliente con ID '{client_id}' no fue encontrado.",
            code="CLIENTE_NO_ENCONTRADO",
            details={
                "client_id": str(client_id)
            }
        )
