from uuid import UUID
from app.common.exceptions import ValidationException

class PurchaseAlreadyExistsException(ValidationException):
    """
    Exception raised when a purchase with the same invoice number already exists for a supplier.
    """
    def __init__(self, invoice_number: str, supplier_id: UUID):
        super().__init__(
            message=f"A purchase with invoice number '{invoice_number}' already exists for supplier '{supplier_id}'.",
            code="PURCHASE_ALREADY_EXISTS",
            details={
                "invoice_number": invoice_number,
                "supplier_id": str(supplier_id)
            }
        )
