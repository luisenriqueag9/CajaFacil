from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.data.repositories.caja_repository_impl import CajaRepositoryImpl
from app.modules.caja.application.event_dispatcher import EventDispatcher

from app.modules.caja.application.use_cases import (
    AbrirCajaUseCase,
    RegistrarMovimientoCajaUseCase,
    RegistrarArqueoCajaUseCase,
    CerrarCajaUseCase,
    ObtenerSaldoCajaUseCase,
    ObtenerCajaActivaUseCase
)

def get_caja_repository(db: Session = Depends(get_db)) -> CajaRepository:
    return CajaRepositoryImpl(db)

def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()

def get_abrir_caja_use_case(
    repository: CajaRepository = Depends(get_caja_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AbrirCajaUseCase:
    return AbrirCajaUseCase(repository, db, event_dispatcher)

def get_registrar_movimiento_use_case(
    repository: CajaRepository = Depends(get_caja_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarMovimientoCajaUseCase:
    return RegistrarMovimientoCajaUseCase(repository, db, event_dispatcher)

def get_registrar_arqueo_use_case(
    repository: CajaRepository = Depends(get_caja_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarArqueoCajaUseCase:
    return RegistrarArqueoCajaUseCase(repository, db, event_dispatcher)

def get_cerrar_caja_use_case(
    repository: CajaRepository = Depends(get_caja_repository),
    db: Session = Depends(get_db),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> CerrarCajaUseCase:
    return CerrarCajaUseCase(repository, db, event_dispatcher)

def get_obtener_saldo_use_case(
    repository: CajaRepository = Depends(get_caja_repository)
) -> ObtenerSaldoCajaUseCase:
    return ObtenerSaldoCajaUseCase(repository)

def get_obtener_caja_activa_use_case(
    repository: CajaRepository = Depends(get_caja_repository)
) -> ObtenerCajaActivaUseCase:
    return ObtenerCajaActivaUseCase(repository)
