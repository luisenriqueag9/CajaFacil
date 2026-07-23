from uuid import UUID
from app.common.exceptions import NotFoundException

class PurchaseNotFoundException(NotFoundException):
    """
    Exception raised when a requested purchase does not exist.
    """
    def __init__(self, purchase_id: UUID):
        super().__init__(
            message=f"Purchase with id '{purchase_id}' was not found.",
            code="PURCHASE_NOT_FOUND",
            details={
                "purchase_id": str(purchase_id)
            }
        )
