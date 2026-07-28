from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.infrastructure.persistence.repositories.caja_repository_impl import CajaRepositoryImpl
from app.modules.caja.infrastructure.persistence.repositories.sesion_caja_repository_impl import SesionCajaRepositoryImpl
from app.modules.caja.application.ports.unit_of_work import UnitOfWork
from app.modules.caja.infrastructure.unit_of_work.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork
from app.common.event_dispatcher import EventDispatcher

from app.modules.caja.application.use_cases import (
    AbrirSesionUseCase,
    CerrarSesionUseCase,
    RegistrarMovimientoUseCase,
    RegistrarArqueoUseCase,
    AnularMovimientoUseCase,
    ObtenerSesionUseCase,
    ListarSesionesUseCase,
    # Legacy names compatibility
    AbrirCajaUseCase,
    RegistrarMovimientoCajaUseCase,
    RegistrarArqueoCajaUseCase,
    CerrarCajaUseCase,
    ObtenerCajaActivaUseCase,
)

def get_caja_repository(db: Session = Depends(get_db)) -> CajaRepository:
    return CajaRepositoryImpl(db)

def get_sesion_caja_repository(db: Session = Depends(get_db)) -> SesionCajaRepository:
    return SesionCajaRepositoryImpl(db)

def get_unit_of_work(db: Session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(db)

def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()

# New clean dependencies
def get_abrir_sesion_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    caja_repository: CajaRepository = Depends(get_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AbrirSesionUseCase:
    return AbrirSesionUseCase(repository, caja_repository, uow, event_dispatcher)

def get_cerrar_sesion_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> CerrarSesionUseCase:
    return CerrarSesionUseCase(repository, uow, event_dispatcher)

def get_registrar_movimiento_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarMovimientoUseCase:
    return RegistrarMovimientoUseCase(repository, uow, event_dispatcher)

def get_registrar_arqueo_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarArqueoUseCase:
    return RegistrarArqueoUseCase(repository, uow, event_dispatcher)

def get_anular_movimiento_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AnularMovimientoUseCase:
    return AnularMovimientoUseCase(repository, uow, event_dispatcher)

def get_obtener_sesion_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository)
) -> ObtenerSesionUseCase:
    return ObtenerSesionUseCase(repository)

def get_listar_sesiones_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository)
) -> ListarSesionesUseCase:
    return ListarSesionesUseCase(repository)


# Legacy bindings for existing modules compatibility (e.g. Venta dependencies, etc)
def get_abrir_caja_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    caja_repository: CajaRepository = Depends(get_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AbrirCajaUseCase:
    return AbrirSesionUseCase(repository, caja_repository, uow, event_dispatcher)

def get_cerrar_caja_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> CerrarCajaUseCase:
    return CerrarSesionUseCase(repository, uow, event_dispatcher)

def get_obtener_caja_activa_use_case(
    repository: SesionCajaRepository = Depends(get_sesion_caja_repository)
) -> ObtenerCajaActivaUseCase:
    return ObtenerSesionUseCase(repository)
