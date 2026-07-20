from app.modules.company.domain.entities.company import Company
from app.modules.company.domain.repositories.company_repository import CompanyRepository
from app.modules.company.domain.exceptions import CompanyAlreadyExistsException


class CreateCompanyUseCase:
    """
    Use case responsible for creating a new Company.
    Applies all business rules before persisting data.
    """

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, company: Company) -> Company:
        """
        Creates a company after validating business rules.
        """

        existing_company = self.repository.get_by_tax_id(company.tax_id)

        if existing_company is not None:
            raise CompanyAlreadyExistsException(company.tax_id)

        return self.repository.create(company)