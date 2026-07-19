from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class CajaFacilException(Exception):
    """
    Base Exception class for CajaFácil Application.
    Inherited by all custom exceptions to allow unified middleware handling.
    """
    def __init__(
        self, 
        message: str, 
        code: str = "INTERNAL_SERVER_ERROR", 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Any] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)

class NotFoundException(CajaFacilException):
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND", details: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_404_NOT_FOUND, details)

class ValidationException(CajaFacilException):
    def __init__(self, message: str = "Validation failed", code: str = "VALIDATION_ERROR", details: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_400_BAD_REQUEST, details)

class UnauthorizedException(CajaFacilException):
    def __init__(self, message: str = "Unauthorized access", code: str = "UNAUTHORIZED", details: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_401_UNAUTHORIZED, details)

class ForbiddenException(CajaFacilException):
    def __init__(self, message: str = "Permission denied", code: str = "FORBIDDEN", details: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_403_FORBIDDEN, details)
