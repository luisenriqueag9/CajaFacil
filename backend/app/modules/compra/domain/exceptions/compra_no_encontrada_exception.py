from uuid import UUID
from app.common.exceptions import NotFoundException

class CompraNoEncontradaException(NotFoundException):
    """
    Excepcion lanzada cuando la compra solicitada no existe.
    """
    def __init__(self, purchase_id: UUID):
        super().__init__(
            message=f"La compra con ID '{purchase_id}' no fue encontrada.",
            code="COMPRA_NO_ENCONTRADA",
            details={
                "purchase_id": str(purchase_id)
            }
        )
