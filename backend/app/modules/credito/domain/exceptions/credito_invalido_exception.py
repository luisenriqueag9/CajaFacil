from app.common.exceptions import ValidationException

class CreditoInvalidoException(ValidationException):
    """
    Excepcion lanzada cuando se violan las invariantes del credito.
    """
    def __init__(self, message: str = "Datos de credito invalidos", details: dict | None = None):
        super().__init__(
            message=message,
            code="CREDITO_INVALIDO",
            details=details
        )
