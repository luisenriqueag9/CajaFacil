from app.modules.company.domain.entities.company import Company
from app.modules.company.domain.repositories.company_repository import CompanyRepository


class GetAllCompaniesUseCase:
    """
    Application use case responsible for retrieving all registered companies.
    """

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(self) -> list[Company]:
        return self.repository.get_all()
    