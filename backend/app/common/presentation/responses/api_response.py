from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """Standardized API Response wrapper for the entire CajaFácil system."""
    success: bool
    message: str
    data: T | None = None

    # Prepared structure to support future properties:
    # errors: list[any] | None = None
    # metadata: dict[str, any] | None = None
    # pagination: any | None = None
