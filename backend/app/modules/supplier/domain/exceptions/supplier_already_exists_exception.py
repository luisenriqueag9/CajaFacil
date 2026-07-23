from uuid import UUID
from app.common.exceptions import ValidationException

class SupplierAlreadyExistsException(ValidationException):
    """
    Exception raised when a supplier with the same Tax ID already exists in the company.
    """
    def __init__(self, tax_id: str, company_id: UUID):
        super().__init__(
            message=f"A supplier with tax identification '{tax_id}' already exists in company '{company_id}'.",
            code="SUPPLIER_ALREADY_EXISTS",
            details={
                "tax_id": tax_id,
                "company_id": str(company_id)
            }
        )
