from app.common.exceptions import ValidationException


class CompanyAlreadyExistsException(ValidationException):
    """
    Exception raised when attempting to create a company
    with a tax identifier that already exists.
    """

    def __init__(self, tax_id: str):
        super().__init__(
            message=f"A company with tax_id '{tax_id}' already exists.",
            code="COMPANY_ALREADY_EXISTS",
            details={
                "tax_id": tax_id
            }
        )