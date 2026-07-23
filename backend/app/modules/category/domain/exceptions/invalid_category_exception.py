from app.common.exceptions import ValidationException

class InvalidCategoryException(ValidationException):
    """
    Exception raised when category details or business rules are violated.
    """
    def __init__(self, message: str = "Invalid category details", details: dict | None = None):
        super().__init__(
            message=message,
            code="INVALID_CATEGORY",
            details=details
        )
