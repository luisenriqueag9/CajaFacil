from app.common.exceptions import ValidationException

class InvalidPurchaseException(ValidationException):
    """
    Exception raised when purchase invariants or business rules are violated.
    """
    def __init__(self, message: str = "Invalid purchase details", details: dict | None = None):
        super().__init__(
            message=message,
            code="INVALID_PURCHASE",
            details=details
        )
