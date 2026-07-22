from uuid import UUID
from app.common.exceptions import ValidationException

class BrandAlreadyExistsException(ValidationException):
    """
    Exception raised when attempting to create/update a brand with a name that already exists for the company.
    """
    def __init__(self, name: str, company_id: UUID):
        super().__init__(
            message=f"A brand with name '{name}' already exists in company '{company_id}'.",
            code="BRAND_ALREADY_EXISTS",
            details={
                "name": name,
                "company_id": str(company_id)
            }
        )
