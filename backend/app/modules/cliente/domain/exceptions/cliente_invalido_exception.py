from app.common.exceptions import ValidationException

class ClienteInvalidoException(ValidationException):
    """
    Excepcion lanzada cuando se violan las invariantes o reglas de negocio del cliente.
    """
    def __init__(self, message: str = "Datos de cliente invalidos", details: dict | None = None):
        super().__init__(
            message=message,
            code="CLIENTE_INVALIDO",
            details=details
        )
