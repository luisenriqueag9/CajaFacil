from app.common.exceptions import ValidationException

class CompraInvalidaException(ValidationException):
    """
    Excepcion lanzada cuando se violan las invariantes o reglas de negocio de la compra.
    """
    def __init__(self, message: str = "Detalles de compra invalidos", details: dict | None = None):
        super().__init__(
            message=message,
            code="COMPRA_INVALIDA",
            details=details
        )
