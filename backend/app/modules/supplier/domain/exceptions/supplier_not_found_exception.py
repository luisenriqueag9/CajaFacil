from uuid import UUID
from app.common.exceptions import NotFoundException

class SupplierNotFoundException(NotFoundException):
    """
    Exception raised when a requested supplier does not exist.
    """
    def __init__(self, supplier_id: UUID):
        super().__init__(
            message=f"Supplier with id '{supplier_id}' was not found.",
            code="SUPPLIER_NOT_FOUND",
            details={
                "supplier_id": str(supplier_id)
            }
        )
