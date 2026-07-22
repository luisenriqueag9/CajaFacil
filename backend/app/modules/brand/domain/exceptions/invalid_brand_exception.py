from app.common.exceptions import ValidationException

class InvalidBrandException(ValidationException):
    """
    Exception raised when brand details or business rules are violated.
    """
    def __init__(self, message: str = "Invalid brand details", details: dict | None = None):
        super().__init__(
            message=message,
            code="INVALID_BRAND",
            details=details
        )
