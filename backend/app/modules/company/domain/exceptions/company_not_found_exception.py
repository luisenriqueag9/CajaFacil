from uuid import UUID

from app.common.exceptions import NotFoundException


class CompanyNotFoundException(NotFoundException):
    """
    Exception raised when the requested company does not exist.
    """

    def __init__(self, company_id: UUID):
        super().__init__(
            message=f"Company with id '{company_id}' was not found.",
            code="COMPANY_NOT_FOUND",
            details={
                "company_id": str(company_id)
            }
        )