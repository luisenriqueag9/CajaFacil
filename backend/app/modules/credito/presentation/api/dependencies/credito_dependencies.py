from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.infrastructure.persistence.repositories.credito_repository_impl import CreditoRepositoryImpl
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.infrastructure.persistence.repositories.cliente_repository_impl import ClienteRepositoryImpl
from app.modules.credito.application.ports.unit_of_work import UnitOfWork
from app.modules.credito.infrastructure.unit_of_work.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork

from app.modules.credito.application.use_cases import (
    AbrirCuentaCreditoUseCase,
    ActualizarLimiteCreditoUseCase,
    InactivarCuentaCreditoUseCase,
    ObtenerCreditoUseCase,
    ListarCreditosUseCase,
    RegistrarCargoCreditoUseCase,
    ReversarCargoCreditoUseCase,
)
from app.common.event_dispatcher import EventDispatcher

def get_credito_repository(db: Session = Depends(get_db)) -> CreditoRepository:
    return CreditoRepositoryImpl(db)

def get_cliente_repository(db: Session = Depends(get_db)) -> ClienteRepository:
    return ClienteRepositoryImpl(db)

def get_unit_of_work(db: Session = Depends(get_db)) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(db)

def get_event_dispatcher() -> EventDispatcher:
    return EventDispatcher()

def get_abrir_cuenta_use_case(
    repository: CreditoRepository = Depends(get_credito_repository),
    cliente_repository: ClienteRepository = Depends(get_cliente_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> AbrirCuentaCreditoUseCase:
    return AbrirCuentaCreditoUseCase(
        repository=repository,
        cliente_repository=cliente_repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_actualizar_limite_use_case(
    repository: CreditoRepository = Depends(get_credito_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> ActualizarLimiteCreditoUseCase:
    return ActualizarLimiteCreditoUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_inactivar_cuenta_use_case(
    repository: CreditoRepository = Depends(get_credito_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> InactivarCuentaCreditoUseCase:
    return InactivarCuentaCreditoUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_obtener_credito_use_case(
    repository: CreditoRepository = Depends(get_credito_repository)
) -> ObtenerCreditoUseCase:
    return ObtenerCreditoUseCase(repository)

def get_listar_creditos_use_case(
    repository: CreditoRepository = Depends(get_credito_repository)
) -> ListarCreditosUseCase:
    return ListarCreditosUseCase(repository)

def get_registrar_cargo_use_case(
    repository: CreditoRepository = Depends(get_credito_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> RegistrarCargoCreditoUseCase:
    return RegistrarCargoCreditoUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )

def get_reversar_cargo_use_case(
    repository: CreditoRepository = Depends(get_credito_repository),
    uow: UnitOfWork = Depends(get_unit_of_work),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher)
) -> ReversarCargoCreditoUseCase:
    return ReversarCargoCreditoUseCase(
        repository=repository,
        uow=uow,
        event_dispatcher=event_dispatcher
    )
