from uuid import UUID
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload

from app.database.repositories import BaseRepository
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria as DomainConfig
from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository
from app.modules.tributacion.data.models import ConfiguracionTributaria as DBConfig
from app.modules.tributacion.data.mappers import tributacion_mapper

class ConfiguracionTributariaRepositoryImpl(BaseRepository[DBConfig], ConfiguracionTributariaRepository):
    """
    Concrete implementation of ConfiguracionTributariaRepository interface using SQLAlchemy.
    Saves and operates on database session utilizing flushes without committing automatically,
    respecting Unit of Work transaction coordination.
    """
    def __init__(self, db: Session):
        super().__init__(DBConfig, db)

    def save(self, config: DomainConfig) -> DomainConfig:
        statement = select(DBConfig).where(DBConfig.id == config.id).options(
            joinedload(DBConfig.rates)
        )
        db_config = self.db.execute(statement).unique().scalar_one_or_none()

        if db_config is not None:
            # Update existing
            tributacion_mapper.update_db_model(db_config, config)
            self.db.flush()
            self.db.refresh(db_config)
            return tributacion_mapper.to_domain(db_config)
        else:
            # Create new
            db_config = tributacion_mapper.to_db(config)
            self.db.add(db_config)
            self.db.flush()
            # Fetch loaded relationships
            db_config_loaded = self.db.execute(statement).unique().scalar_one()
            return tributacion_mapper.to_domain(db_config_loaded)

    def get_by_id(self, config_id: UUID) -> Optional[DomainConfig]:
        statement = select(DBConfig).where(DBConfig.id == config_id).options(
            joinedload(DBConfig.rates)
        )
        db_config = self.db.execute(statement).unique().scalar_one_or_none()
        return tributacion_mapper.to_domain(db_config) if db_config else None

    def get_active_by_company(self, company_id: UUID) -> Optional[DomainConfig]:
        statement = select(DBConfig).where(
            and_(
                DBConfig.company_id == company_id,
                DBConfig.is_active == True
            )
        ).options(
            joinedload(DBConfig.rates)
        )
        db_config = self.db.execute(statement).unique().scalar_one_or_none()
        return tributacion_mapper.to_domain(db_config) if db_config else None

    def search(self, company_id: UUID, filters: dict) -> List[DomainConfig]:
        statement = select(DBConfig).where(DBConfig.company_id == company_id).options(
            joinedload(DBConfig.rates)
        )

        # Apply filters
        if "is_active" in filters and filters["is_active"] is not None:
            statement = statement.where(DBConfig.is_active == filters["is_active"])

        statement = statement.order_by(DBConfig.valid_from.desc())
        db_configs = self.db.execute(statement).unique().scalars().all()
        return [tributacion_mapper.to_domain(c) for c in db_configs]
