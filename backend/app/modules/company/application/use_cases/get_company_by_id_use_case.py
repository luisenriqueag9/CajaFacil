from uuid import UUID

from app.modules.company.domain.entities.company import Company
from app.modules.company.domain.repositories.company_repository import CompanyRepository
from app.modules.company.domain.exceptions.company_not_found_exception import (
    CompanyNotFoundException,
)


class GetCompanyByIdUseCase:
    """
    Use case responsible for retrieving a company by its unique identifier.
    """

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, company_id: UUID) -> Company:
        """
        Retrieves a company by its unique identifier.
        Raises CompanyNotFoundException if the company does not exist.
        """

        company = self.repository.get_by_id(company_id)

        if company is None:
            raise CompanyNotFoundException(company_id)

        return company