from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.database.repositories.base import BaseRepository
from app.modules.caja.domain.aggregates.sesion_caja import SesionCaja
from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.infrastructure.persistence.models.caja_model import SesionCaja as DBOSesionCaja
from app.modules.caja.infrastructure.persistence.mappers.caja_mapper import CajaMapper
from app.modules.caja.domain.exceptions.caja_exceptions import SesionCajaNotFoundException

class SesionCajaRepositoryImpl(BaseRepository[DBOSesionCaja], SesionCajaRepository):
    """
    Implementacion de SesionCajaRepository utilizando SQLAlchemy.
    Maneja las sesiones/turnos activos e historicos.
    """
    def __init__(self, db: Session):
        super().__init__(DBOSesionCaja, db)

    def create(self, sesion: SesionCaja) -> SesionCaja:
        db_session = CajaMapper.sesion_to_db(sesion)
        self.db.add(db_session)
        self.db.flush()
        return CajaMapper.sesion_to_domain(db_session)

    def get_by_id(self, sesion_id: UUID) -> SesionCaja | None:
        statement = select(DBOSesionCaja).where(DBOSesionCaja.id == sesion_id)
        db_session = self.db.execute(statement).scalar_one_or_none()
        return CajaMapper.sesion_to_domain(db_session) if db_session else None

    def get_active_by_user(self, company_id: UUID, user_id: UUID) -> SesionCaja | None:
        statement = select(DBOSesionCaja).where(
            and_(
                DBOSesionCaja.company_id == company_id,
                DBOSesionCaja.user_id == user_id,
                DBOSesionCaja.status == "ABIERTA"
            )
        )
        db_session = self.db.execute(statement).scalar_one_or_none()
        return CajaMapper.sesion_to_domain(db_session) if db_session else None

    def get_active_by_caja(self, company_id: UUID, caja_id: UUID) -> SesionCaja | None:
        statement = select(DBOSesionCaja).where(
            and_(
                DBOSesionCaja.company_id == company_id,
                DBOSesionCaja.caja_id == caja_id,
                DBOSesionCaja.status == "ABIERTA"
            )
        )
        db_session = self.db.execute(statement).scalar_one_or_none()
        return CajaMapper.sesion_to_domain(db_session) if db_session else None

    def get_all(self, company_id: UUID, status: str | None = None) -> list[SesionCaja]:
        statement = select(DBOSesionCaja).where(DBOSesionCaja.company_id == company_id)
        if status:
            statement = statement.where(DBOSesionCaja.status == status)
        
        statement = statement.order_by(DBOSesionCaja.opened_at.desc())
        db_sessions = self.db.execute(statement).scalars().all()
        return [CajaMapper.sesion_to_domain(s) for s in db_sessions]

    def update(self, sesion: SesionCaja) -> SesionCaja:
        statement = select(DBOSesionCaja).where(DBOSesionCaja.id == sesion.id)
        db_session = self.db.execute(statement).scalar_one_or_none()
        if not db_session:
            raise SesionCajaNotFoundException(sesion.id)

        CajaMapper.update_sesion_db_model(db_session, sesion)
        self.db.flush()
        self.db.refresh(db_session)
        return CajaMapper.sesion_to_domain(db_session)
