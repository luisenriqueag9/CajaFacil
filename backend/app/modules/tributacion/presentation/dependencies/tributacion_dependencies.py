from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository
from app.modules.tributacion.data.repositories.configuracion_repository_impl import ConfiguracionTributariaRepositoryImpl
from app.modules.tributacion.application.event_dispatcher import EventDispatcher

from app.modules.tributacion.application.use_cases import (
    CrearConfiguracionTributariaUseCase,
    ActivarConfiguracionTributariaUseCase,
    ObtenerConfiguracionActivaUseCase,
    CalcularImpuestoTransaccionUseCase
)

def get_configuracion_repository(db: Session = Depends(get_db)) -> ConfiguracionTributariaRepository:
    return ConfiguracionTributariaRepositoryImpl(db)

def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()

def get_crear_configuracion_use_case(
    repository: ConfiguracionTributariaRepository = Depends(get_configuracion_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> CrearConfiguracionTributariaUseCase:
    return CrearConfiguracionTributariaUseCase(repository, db, event_dispatcher)

def get_activar_configuracion_use_case(
    repository: ConfiguracionTributariaRepository = Depends(get_configuracion_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> ActivarConfiguracionTributariaUseCase:
    return ActivarConfiguracionTributariaUseCase(repository, db, event_dispatcher)

def get_obtener_configuracion_activa_use_case(
    repository: ConfiguracionTributariaRepository = Depends(get_configuracion_repository)
) -> ObtenerConfiguracionActivaUseCase:
    return ObtenerConfiguracionActivaUseCase(repository)

def get_calcular_impuesto_use_case(
    repository: ConfiguracionTributariaRepository = Depends(get_configuracion_repository)
) -> CalcularImpuestoTransaccionUseCase:
    return CalcularImpuestoTransaccionUseCase(repository)
