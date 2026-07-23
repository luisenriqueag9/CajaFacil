from app.common.exceptions import ValidationException

class InvalidSupplierException(ValidationException):
    """
    Exception raised when supplier details or business rules are violated.
    """
    def __init__(self, message: str = "Invalid supplier details", details: dict | None = None):
        super().__init__(
            message=message,
            code="INVALID_SUPPLIER",
            details=details
        )
