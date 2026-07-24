from uuid import UUID
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.database.repositories import BaseRepository
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto as DomainExistencia
from app.modules.inventario.domain.repositories.existencia_repository import ExistenciaRepository
from app.modules.inventario.data.models import ExistenciaProducto as DBExistencia
from app.modules.inventario.data.mappers import existencia_mapper

class ExistenciaRepositoryImpl(BaseRepository[DBExistencia], ExistenciaRepository):
    """
    Concrete implementation of ExistenciaRepository using SQLAlchemy.
    Saves and operates on database session utilizing flushes without committing automatically,
    respecting Unit of Work transaction coordination.
    """
    def __init__(self, db: Session):
        super().__init__(DBExistencia, db)

    def save(self, existencia: DomainExistencia) -> DomainExistencia:
        statement = select(DBExistencia).where(
            and_(
                DBExistencia.company_id == existencia.company_id,
                DBExistencia.product_id == existencia.product_id
            )
        )
        db_existencia = self.db.execute(statement).scalar_one_or_none()

        if db_existencia is not None:
            # Update existing
            existencia_mapper.update_db_model(db_existencia, existencia)
            self.db.flush()
            self.db.refresh(db_existencia)
            return existencia_mapper.to_domain(db_existencia)
        else:
            # Create new
            db_existencia = existencia_mapper.to_db(existencia)
            self.db.add(db_existencia)
            self.db.flush()
            self.db.refresh(db_existencia)
            return existencia_mapper.to_domain(db_existencia)

    def get_by_product_id(self, company_id: UUID, product_id: UUID) -> Optional[DomainExistencia]:
        statement = select(DBExistencia).where(
            and_(
                DBExistencia.company_id == company_id,
                DBExistencia.product_id == product_id
            )
        )
        db_existencia = self.db.execute(statement).scalar_one_or_none()
        return existencia_mapper.to_domain(db_existencia) if db_existencia else None

    def search(self, company_id: UUID, filters: dict) -> List[DomainExistencia]:
        statement = select(DBExistencia).where(DBExistencia.company_id == company_id)
        
        # Optionally support filtering by product list or low stock
        if "product_ids" in filters and filters["product_ids"]:
            statement = statement.where(DBExistencia.product_id.in_(filters["product_ids"]))

        db_existencias = self.db.execute(statement).scalars().all()
        return [existencia_mapper.to_domain(e) for e in db_existencias]
