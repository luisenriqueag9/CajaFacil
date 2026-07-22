from uuid import UUID
from app.common.exceptions import ValidationException

class ProductAlreadyExistsException(ValidationException):
    """
    Exception raised when attempting to create a product
    with an internal_code or barcode that already exists for the company.
    """
    def __init__(self, key: str, value: str, company_id: UUID):
        super().__init__(
            message=f"A product with {key} '{value}' already exists in company '{company_id}'.",
            code="PRODUCT_ALREADY_EXISTS",
            details={
                "key": key,
                "value": value,
                "company_id": str(company_id)
            }
        )
