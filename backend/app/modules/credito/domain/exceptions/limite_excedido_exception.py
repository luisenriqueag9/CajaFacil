from app.common.exceptions import ValidationException

class LimiteExcedidoException(ValidationException):
    """
    Excepcion lanzada cuando el saldo deudor supera el limite de credito permitido.
    """
    def __init__(self, message: str = "Limite de credito excedido", details: dict | None = None):
        super().__init__(
            message=message,
            code="LIMITE_CREDITO_EXCEDIDO",
            details=details
        )
