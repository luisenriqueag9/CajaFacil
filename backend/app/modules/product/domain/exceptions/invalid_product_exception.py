from app.common.exceptions import ValidationException

class InvalidProductException(ValidationException):
    """
    Exception raised when product details or business rules are violated.
    Inherits from ValidationException to return HTTP 400 automatically.
    """
    def __init__(self, message: str = "Invalid product details", details: dict | None = None):
        super().__init__(
            message=message,
            code="INVALID_PRODUCT",
            details=details
        )
