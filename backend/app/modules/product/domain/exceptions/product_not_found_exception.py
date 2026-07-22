from uuid import UUID
from app.common.exceptions import NotFoundException

class ProductNotFoundException(NotFoundException):
    """
    Exception raised when the requested product does not exist.
    """
    def __init__(self, product_id: UUID):
        super().__init__(
            message=f"Product with id '{product_id}' was not found.",
            code="PRODUCT_NOT_FOUND",
            details={
                "product_id": str(product_id)
            }
        )
