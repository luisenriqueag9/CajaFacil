import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria, TasaImpuesto
from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository
from app.modules.tributacion.domain.events.tributacion_events import ConfiguracionTributariaCreada
from app.modules.tributacion.application.event_dispatcher import EventDispatcher

@dataclass(frozen=True)
class TasaInput:
    name: str
    code: str
    rate_percentage: Decimal

@dataclass(frozen=True)
class CrearConfiguracionTributariaCommand:
    company_id: uuid.UUID
    name: str
    calculation_type: str  # INCLUIDO, ADICIONADO
    rates: list[TasaInput]

class CrearConfiguracionTributariaUseCase:
    """
    Application Use Case to create a new, inactive Tax Configuration version for a company.
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

    def execute(self, command: CrearConfiguracionTributariaCommand) -> ConfiguracionTributaria:
        config_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        # 1. Instantiate Aggregate Root
        config = ConfiguracionTributaria(
            id=config_id,
            company_id=command.company_id,
            name=command.name,
            is_active=False,
            valid_from=now,
            calculation_type=command.calculation_type,
            rates=[]
        )

        # 2. Add Rates (runs validations)
        for r_in in command.rates:
            tasa = TasaImpuesto(
                id=uuid.uuid4(),
                configuracion_id=config_id,
                name=r_in.name,
                code=r_in.code,
                rate_percentage=r_in.rate_percentage
            )
            config.agregar_tasa(tasa)

        # 3. Save and Dispatch (Unit of Work)
        try:
            with self.db.begin_nested():
                saved_config = self.repository.save(config)
                
                event = ConfiguracionTributariaCreada(
                    configuracion_id=saved_config.id,
                    company_id=saved_config.company_id,
                    valid_from=saved_config.valid_from,
                    occurred_at=now
                )
                self.event_dispatcher.dispatch(event)
            self.db.commit()
            return saved_config
        except Exception as e:
            self.db.rollback()
            raise e
