from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.company.domain.repositories.company_repository import CompanyRepository
from app.modules.company.data.repositories.company_repository_impl import CompanyRepositoryImpl
from app.modules.company.application.use_cases.create_company_use_case import CreateCompanyUseCase

def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepository:
    """FastAPI dependency to retrieve the concrete implementation of CompanyRepository."""
    return CompanyRepositoryImpl(db)

def get_create_company_use_case(
    repository: CompanyRepository = Depends(get_company_repository)
) -> CreateCompanyUseCase:
    """FastAPI dependency to retrieve the CreateCompanyUseCase initialized with its repository."""
    return CreateCompanyUseCase(repository)
