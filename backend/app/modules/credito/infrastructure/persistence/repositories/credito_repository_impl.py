from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.database.repositories.base import BaseRepository
from app.modules.credito.domain.aggregates.credito import Credito
from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.infrastructure.persistence.models.credito_model import Credito as DBOCredito
from app.modules.credito.infrastructure.persistence.mappers.credito_mapper import CreditoMapper
from app.modules.credito.domain.exceptions.credito_no_encontrado_exception import CreditoNoEncontradoException

class CreditoRepositoryImpl(BaseRepository[DBOCredito], CreditoRepository):
    """
    Implementacion concreta de CreditoRepository utilizando SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBOCredito, db)

    def create(self, credito: Credito) -> Credito:
        db_credit = CreditoMapper.to_db(credito)
        self.db.add(db_credit)
        self.db.flush()
        return CreditoMapper.to_domain(db_credit)

    def get_by_id(self, credit_id: UUID) -> Credito | None:
        statement = select(DBOCredito).where(DBOCredito.id == credit_id)
        db_credit = self.db.execute(statement).scalar_one_or_none()
        return CreditoMapper.to_domain(db_credit) if db_credit else None

    def get_by_client_id(self, company_id: UUID, client_id: UUID) -> Credito | None:
        statement = select(DBOCredito).where(
            and_(
                DBOCredito.company_id == company_id,
                DBOCredito.client_id == client_id
            )
        )
        db_credit = self.db.execute(statement).scalar_one_or_none()
        return CreditoMapper.to_domain(db_credit) if db_credit else None

    def get_all(self, company_id: UUID, status: str | None = None) -> list[Credito]:
        statement = select(DBOCredito).where(DBOCredito.company_id == company_id)
        if status:
            statement = statement.where(DBOCredito.status == status)
            
        statement = statement.order_by(DBOCredito.created_at.desc())
        db_credits = self.db.execute(statement).scalars().all()
        return [CreditoMapper.to_domain(c) for c in db_credits]

    def update(self, credito: Credito) -> Credito:
        statement = select(DBOCredito).where(DBOCredito.id == credito.id)
        db_credit = self.db.execute(statement).scalar_one_or_none()
        if not db_credit:
            raise CreditoNoEncontradoException(credito.id)

        CreditoMapper.update_db_model(db_credit, credito)
        self.db.flush()
        self.db.refresh(db_credit)
        return CreditoMapper.to_domain(db_credit)
