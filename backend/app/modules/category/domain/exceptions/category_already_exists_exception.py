from uuid import UUID
from app.common.exceptions import ValidationException

class CategoryAlreadyExistsException(ValidationException):
    """
    Exception raised when a category with the same name already exists in the company.
    """
    def __init__(self, name: str, company_id: UUID):
        super().__init__(
            message=f"A category with name '{name}' already exists in company '{company_id}'.",
            code="CATEGORY_ALREADY_EXISTS",
            details={
                "name": name,
                "company_id": str(company_id)
            }
        )
