from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class BaseAPIResponse(BaseModel):
    """
    Standard top-level envelope structure for all successful API responses.
    """
    success: bool = True
    message: Optional[str] = "Success"

class APIResponse(BaseAPIResponse, Generic[T]):
    """
    Wrapper for API responses returning a data payload of type T.
    """
    data: Optional[T] = None

class APIErrorResponse(BaseModel):
    """
    Standard error envelope structure for API responses.
    """
    success: bool = False
    error_code: str
    message: str
    details: Optional[any] = None
