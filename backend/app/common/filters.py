from typing import Optional
from pydantic import BaseModel, Field

class BaseFilterParams(BaseModel):
    """
    Standard filtering and sorting query parameters.
    """
    search: Optional[str] = Field(default=None, description="Global search query string")
    sort_by: Optional[str] = Field(default=None, description="Field name to sort by")
    sort_order: Optional[str] = Field(default="asc", description="Sort direction: 'asc' or 'desc'")
