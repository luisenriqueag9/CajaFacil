from uuid import UUID
from pydantic import BaseModel, ConfigDict

class POSProductSearchResponse(BaseModel):
    """Projection DTO representing the minimal product details required by the POS search view."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    price: float
