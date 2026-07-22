from uuid import UUID
from app.common.exceptions import NotFoundException

class BrandNotFoundException(NotFoundException):
    """
    Exception raised when the requested brand does not exist.
    """
    def __init__(self, brand_id: UUID):
        super().__init__(
            message=f"Brand with id '{brand_id}' was not found.",
            code="BRAND_NOT_FOUND",
            details={
                "brand_id": str(brand_id)
            }
        )
