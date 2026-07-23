from uuid import UUID
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload

from app.database.repositories import BaseRepository
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario as DomainMovimiento
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository
from app.modules.inventario.data.models import MovimientoInventario as DBMovimiento
from app.modules.inventario.data.mappers import movimiento_mapper

class MovimientoInventarioRepositoryImpl(BaseRepository[DBMovimiento], MovimientoInventarioRepository):
    """
    Concrete implementation of MovimientoInventarioRepository interface using SQLAlchemy.
    Saves changes into current active session utilizing flushes without committing automatically,
    respecting Unit of Work transaction coordination.
    """
    def __init__(self, db: Session):
        super().__init__(DBMovimiento, db)

    def save(self, movimiento: DomainMovimiento) -> DomainMovimiento:
        db_mov = movimiento_mapper.to_db(movimiento)
        self.db.add(db_mov)
        self.db.flush()

        # Re-fetch to ensure relationships are loaded
        statement = select(DBMovimiento).where(DBMovimiento.id == movimiento.id).options(
            joinedload(DBMovimiento.merma),
            joinedload(DBMovimiento.ajuste)
        )
        db_mov_loaded = self.db.execute(statement).unique().scalar_one()
        return movimiento_mapper.to_domain(db_mov_loaded)

    def get_by_id(self, movimiento_id: UUID) -> Optional[DomainMovimiento]:
        statement = select(DBMovimiento).where(DBMovimiento.id == movimiento_id).options(
            joinedload(DBMovimiento.merma),
            joinedload(DBMovimiento.ajuste)
        )
        db_mov = self.db.execute(statement).unique().scalar_one_or_none()
        return movimiento_mapper.to_domain(db_mov) if db_mov else None

    def get_by_product_id(self, company_id: UUID, product_id: UUID) -> List[DomainMovimiento]:
        statement = select(DBMovimiento).where(
            and_(
                DBMovimiento.company_id == company_id,
                DBMovimiento.product_id == product_id
            )
        ).options(
            joinedload(DBMovimiento.merma),
            joinedload(DBMovimiento.ajuste)
        ).order_by(DBMovimiento.created_at.asc())  # Ascending for chronological stock reconstruction
        
        db_movs = self.db.execute(statement).unique().scalars().all()
        return [movimiento_mapper.to_domain(m) for m in db_movs]

    def search(self, company_id: UUID, filters: dict) -> List[DomainMovimiento]:
        statement = select(DBMovimiento).where(DBMovimiento.company_id == company_id).options(
            joinedload(DBMovimiento.merma),
            joinedload(DBMovimiento.ajuste)
        )

        # Filters application
        if "product_id" in filters and filters["product_id"]:
            statement = statement.where(DBMovimiento.product_id == filters["product_id"])
        if "type" in filters and filters["type"]:
            statement = statement.where(DBMovimiento.type == filters["type"])
        if "concept" in filters and filters["concept"]:
            statement = statement.where(DBMovimiento.concept == filters["concept"])
        if "created_by" in filters and filters["created_by"]:
            statement = statement.where(DBMovimiento.created_by == filters["created_by"])
        if "start_date" in filters and filters["start_date"]:
            statement = statement.where(DBMovimiento.created_at >= filters["start_date"])
        if "end_date" in filters and filters["end_date"]:
            statement = statement.where(DBMovimiento.created_at <= filters["end_date"])

        statement = statement.order_by(DBMovimiento.created_at.desc())
        db_movs = self.db.execute(statement).unique().scalars().all()
        return [movimiento_mapper.to_domain(m) for m in db_movs]
