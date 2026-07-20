from app.modules.company.domain.entities.company import Company
from app.modules.company.domain.repositories.company_repository import CompanyRepository

class CreateCompanyUseCase:
    """Use case to handle creation of a new Company in the system."""
    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self, company: Company) -> Company:
        """Executes the business logic to create a new company entity."""
        return self.repository.create(company)
