from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.repositories.base import BaseRepository
from app.modules.caja.domain.entities.caja import Caja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.infrastructure.persistence.models.caja_model import Caja as DBOCaja
from app.modules.caja.infrastructure.persistence.mappers.caja_mapper import CajaMapper

class CajaRepositoryImpl(BaseRepository[DBOCaja], CajaRepository):
    """
    Implementacion de CajaRepository utilizando SQLAlchemy.
    Maneja las cajas fisicas disponibles.
    """
    def __init__(self, db: Session):
        super().__init__(DBOCaja, db)

    def create(self, caja: Caja) -> Caja:
        db_caja = CajaMapper.caja_to_db(caja)
        self.db.add(db_caja)
        self.db.flush()
        return CajaMapper.caja_to_domain(db_caja)

    def get_by_id(self, caja_id: UUID) -> Caja | None:
        statement = select(DBOCaja).where(DBOCaja.id == caja_id)
        db_caja = self.db.execute(statement).scalar_one_or_none()
        return CajaMapper.caja_to_domain(db_caja) if db_caja else None

    def get_all(self, company_id: UUID) -> list[Caja]:
        statement = select(DBOCaja).where(DBOCaja.company_id == company_id).order_by(DBOCaja.name.asc())
        db_cajas = self.db.execute(statement).scalars().all()
        return [CajaMapper.caja_to_domain(c) for c in db_cajas]
