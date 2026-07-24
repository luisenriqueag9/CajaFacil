import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository
from app.modules.tributacion.domain.exceptions import ConfiguracionNotFoundException
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria
from app.modules.tributacion.domain.events.tributacion_events import (
    ConfiguracionTributariaActivada,
    ConfiguracionTributariaDesactivada
)
from app.modules.tributacion.application.event_dispatcher import EventDispatcher

class ActivarConfiguracionTributariaUseCase:
    """
    Application Use Case to activate a specific tax configuration version,
    deactivating the previously active version to maintain exclusivity rules.
    """
    def __init__(
        self,
        repository: ConfiguracionTributariaRepository,
        db: Session,
        event_dispatcher: EventDispatcher
    ):
        self.repository = repository
        self.db = db
        self.event_dispatcher = event_dispatcher

    def execute(self, company_id: uuid.UUID, configuracion_id: uuid.UUID) -> ConfiguracionTributaria:
        # 1. Fetch target config
        target_config = self.repository.get_by_id(configuracion_id)
        if target_config is None or target_config.company_id != company_id:
            raise ConfiguracionNotFoundException(configuracion_id)

        if target_config.is_active:
            return target_config

        now = datetime.now(timezone.utc)

        # 2. Fetch current active config
        current_active = self.repository.get_active_by_company(company_id)

        # 3. Sincronize transition (Unit of Work)
        try:
            with self.db.begin_nested():
                if current_active is not None:
                    current_active.desactivar(now)
                    self.repository.save(current_active)
                    
                    event_deact = ConfiguracionTributariaDesactivada(
                        configuracion_id=current_active.id,
                        company_id=company_id,
                        valid_to=now,
                        occurred_at=now
                    )
                    self.event_dispatcher.dispatch(event_deact)

                target_config.activar(now)
                saved_config = self.repository.save(target_config)

                event_act = ConfiguracionTributariaActivada(
                    configuracion_id=saved_config.id,
                    company_id=company_id,
                    valid_from=now,
                    occurred_at=now
                )
                self.event_dispatcher.dispatch(event_act)

            self.db.commit()
            return saved_config
        except Exception as e:
            self.db.rollback()
            raise e
