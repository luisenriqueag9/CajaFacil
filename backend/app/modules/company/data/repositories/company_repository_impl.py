from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.repositories import BaseRepository
from app.modules.company.domain.entities.company import Company as DomainCompany
from app.modules.company.domain.repositories.company_repository import CompanyRepository
from app.modules.company.data.models import Company as DBCompany
from app.modules.company.data.mappers import company_mapper
from app.modules.company.domain.exceptions import CompanyNotFoundException

class CompanyRepositoryImpl(BaseRepository[DBCompany], CompanyRepository):
    def __init__(self, db: Session):
        super().__init__(DBCompany, db)

    def create(self, company: DomainCompany) -> DomainCompany:
        db_company = company_mapper.to_db(company)
        db_company = super().create(db_company)
        self.db.refresh(db_company)
        return company_mapper.to_domain(db_company)
    
    def get_by_tax_id(self, tax_id: str) -> DomainCompany | None:
        """
        Retrieve a company by its tax identifier (RTN).
        Returns None if no company exists.
        """
        statement = select(DBCompany).where(DBCompany.tax_id == tax_id)

        db_company = self.db.execute(statement).scalar_one_or_none()

        if db_company is None:
            return None

        return company_mapper.to_domain(db_company)

    def get_by_id(self, company_id: UUID) -> DomainCompany | None:
        db_company = super().get_by_id(company_id)
        return company_mapper.to_domain(db_company) if db_company else None

    def get_all(self) -> list[DomainCompany]:
        db_companies = super().get_all()
        return [company_mapper.to_domain(c) for c in db_companies]

    def update(self, company: DomainCompany) -> DomainCompany:
        db_company = super().get_by_id(company.id)
        if not db_company:
            raise CompanyNotFoundException(company.id)
        
        company_mapper.update_db_model(db_company, company)
        self.db.flush()
        self.db.refresh(db_company)
        return company_mapper.to_domain(db_company)

