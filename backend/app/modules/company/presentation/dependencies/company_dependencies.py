from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.company.domain.repositories.company_repository import CompanyRepository
from app.modules.company.data.repositories.company_repository_impl import CompanyRepositoryImpl
from app.modules.company.application.use_cases.create_company_use_case import CreateCompanyUseCase
from app.modules.company.application.use_cases.get_company_by_id_use_case import (
    GetCompanyByIdUseCase,
)
from app.modules.company.application.use_cases.get_all_companies_use_case import (
    GetAllCompaniesUseCase,
)
from app.modules.company.application.use_cases.update_company_use_case import (
    UpdateCompanyUseCase,
)

def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepository:
    """FastAPI dependency to retrieve the concrete implementation of CompanyRepository."""
    return CompanyRepositoryImpl(db)

def get_create_company_use_case(
    repository: CompanyRepository = Depends(get_company_repository)
) -> CreateCompanyUseCase:
    """
    Provides the CreateCompanyUseCase dependency.
    """
    return CreateCompanyUseCase(repository)

def get_company_by_id_use_case(
    repository: CompanyRepository = Depends(get_company_repository)
) -> GetCompanyByIdUseCase:
    """
    FastAPI dependency to retrieve the GetCompanyByIdUseCase
    initialized with its repository.
    """
    return GetCompanyByIdUseCase(repository)

def get_all_companies_use_case(
    repository: CompanyRepository = Depends(get_company_repository)
) -> GetAllCompaniesUseCase:
    """
    FastAPI dependency to retrieve the GetAllCompaniesUseCase
    initialized with its repository.
    """
    return GetAllCompaniesUseCase(repository)


def get_update_company_use_case(
    repository: CompanyRepository = Depends(get_company_repository),
) -> UpdateCompanyUseCase:
    """
    FastAPI dependency to retrieve the UpdateCompanyUseCase
    initialized with its repository.
    """
    return UpdateCompanyUseCase(repository)