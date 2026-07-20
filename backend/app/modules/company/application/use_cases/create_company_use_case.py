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

        # Business Rule:
        # A company with the same RTN (tax_id) cannot exist.
        existing_company = self.repository.get_by_tax_id(company.tax_id)
        print("===================================")
        print("TAX_ID:", company.tax_id)
        print("EXISTING COMPANY:", existing_company)
        print("===================================")
        # =========================

        if existing_company is not None:
            raise CompanyAlreadyExistsException(
                f"A company with tax_id '{company.tax_id}' already exists."
            )

        return self.repository.create(company)