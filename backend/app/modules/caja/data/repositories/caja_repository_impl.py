from uuid import UUID
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload

from app.database.repositories import BaseRepository
from app.modules.caja.domain.entities.caja import Caja as DomainCaja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.data.models import Caja as DBCaja
from app.modules.caja.data.mappers import caja_mapper

class CajaRepositoryImpl(BaseRepository[DBCaja], CajaRepository):
    """
    Concrete implementation of CajaRepository interface using SQLAlchemy.
    Saves sessions and operations to SQLAlchemy DB context using flushes without commits,
    complying with the coordinated Unit of Work transaction strategy.
    """
    def __init__(self, db: Session):
        super().__init__(DBCaja, db)

    def save(self, caja: DomainCaja) -> DomainCaja:
        statement = select(DBCaja).where(DBCaja.id == caja.id).options(
            joinedload(DBCaja.movements),
            joinedload(DBCaja.audits)
        )
        db_caja = self.db.execute(statement).unique().scalar_one_or_none()

        if db_caja is not None:
            # Update existing
            caja_mapper.update_db_model(db_caja, caja)
            self.db.flush()
            self.db.refresh(db_caja)
            return caja_mapper.to_domain(db_caja)
        else:
            # Create new
            db_caja = caja_mapper.to_db(caja)
            self.db.add(db_caja)
            self.db.flush()
            # Fetch loaded relationships
            db_caja_loaded = self.db.execute(statement).unique().scalar_one()
            return caja_mapper.to_domain(db_caja_loaded)

    def get_by_id(self, caja_id: UUID) -> Optional[DomainCaja]:
        statement = select(DBCaja).where(DBCaja.id == caja_id).options(
            joinedload(DBCaja.movements),
            joinedload(DBCaja.audits)
        )
        db_caja = self.db.execute(statement).unique().scalar_one_or_none()
        return caja_mapper.to_domain(db_caja) if db_caja else None

    def get_active_by_user(self, company_id: UUID, user_id: UUID) -> Optional[DomainCaja]:
        statement = select(DBCaja).where(
            and_(
                DBCaja.company_id == company_id,
                DBCaja.user_id == user_id,
                DBCaja.status == "OPEN"  # DB stores translated status
            )
        ).options(
            joinedload(DBCaja.movements),
            joinedload(DBCaja.audits)
        )
        db_caja = self.db.execute(statement).unique().scalar_one_or_none()
        return caja_mapper.to_domain(db_caja) if db_caja else None

    def search(self, company_id: UUID, filters: dict) -> List[DomainCaja]:
        statement = select(DBCaja).where(DBCaja.company_id == company_id).options(
            joinedload(DBCaja.movements),
            joinedload(DBCaja.audits)
        )

        # Apply filters
        if "user_id" in filters and filters["user_id"]:
            statement = statement.where(DBCaja.user_id == filters["user_id"])
        if "status" in filters and filters["status"]:
            db_status = caja_mapper.STATUS_TO_DB.get(filters["status"])
            if db_status:
                statement = statement.where(DBCaja.status == db_status)
        if "start_date" in filters and filters["start_date"]:
            statement = statement.where(DBCaja.opened_at >= filters["start_date"])
        if "end_date" in filters and filters["end_date"]:
            statement = statement.where(DBCaja.opened_at <= filters["end_date"])

        statement = statement.order_by(DBCaja.opened_at.desc())
        db_cajas = self.db.execute(statement).unique().scalars().all()
        return [caja_mapper.to_domain(c) for c in db_cajas]
