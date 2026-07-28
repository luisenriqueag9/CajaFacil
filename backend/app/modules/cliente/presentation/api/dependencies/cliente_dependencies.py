from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.infrastructure.persistence.repositories.cliente_repository_impl import ClienteRepositoryImpl
from app.modules.cliente.application.ports.unit_of_work import UnitOfWork
from app.modules.cliente.infrastructure.unit_of_work.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork

from app.modules.cliente.application.use_cases import (
    RegistrarClienteUseCase,
    ActualizarClienteUseCase,
    InactivarClienteUseCase,
    ObtenerClienteUseCase,
    ListarClientesUseCase,
)
from app.common.event_dispatcher import EventDispatcher

def get_cliente_repository(db: Session = Depends(get_db)) -> ClienteRepository:
    return ClienteRepositoryImpl(db)

def get_unit_of_work(db: Session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(db)

def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()

def get_registrar_cliente_use_case(
    repository: ClienteRepository = Depends(get_cliente_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarClienteUseCase:
    return RegistrarClienteUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_actualizar_cliente_use_case(
    repository: ClienteRepository = Depends(get_cliente_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> ActualizarClienteUseCase:
    return ActualizarClienteUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_inactivar_cliente_use_case(
    repository: ClienteRepository = Depends(get_cliente_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> InactivarClienteUseCase:
    return InactivarClienteUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_obtener_cliente_use_case(
    repository: ClienteRepository = Depends(get_cliente_repository)
) -> ObtenerClienteUseCase:
    return ObtenerClienteUseCase(repository)

def get_listar_clientes_use_case(
    repository: ClienteRepository = Depends(get_cliente_repository)
) -> ListarClientesUseCase:
    return ListarClientesUseCase(repository)
