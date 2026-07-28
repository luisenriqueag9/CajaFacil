from datetime import datetime, timezone
from uuid import UUID

from app.modules.compra.domain.aggregates.compra import Compra
from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.domain.exceptions import CompraNoEncontradaException
from app.modules.compra.application.ports.unit_of_work import UnitOfWork
from app.modules.compra.application.commands.anular_compra_command import AnularCompraCommand
from app.modules.compra.application.dto.compra_dto import CompraDTO
from app.modules.compra.application.dto.compra_dto_mapper import CompraDTOMapper
from app.common.event_dispatcher import EventDispatcher

class AnularCompraUseCase:
    """
    Caso de uso para anular una compra registrada.
    """
    def __init__(self, repository: CompraRepository, uow: UnitOfWork, event_dispatcher: EventDispatcher = None):
        self.repository = repository
        
        # Adapt session-like object to UnitOfWork if passed
        if not isinstance(uow, UnitOfWork):
            class SessionUnitOfWork(UnitOfWork):
                def __init__(self, session):
                    self.session = session
                def __enter__(self) -> "SessionUnitOfWork":
                    self.session.begin_nested()
                    return self
                def __exit__(self, exc_type, exc_val, exc_tb) -> None:
                    if exc_type is not None:
                        self.session.rollback()
                    else:
                        self.session.commit()
                def begin(self) -> None:
                    self.session.begin_nested()
                def commit(self) -> None:
                    self.session.commit()
                def rollback(self) -> None:
                    self.session.rollback()
            self.uow = SessionUnitOfWork(uow)
        else:
            self.uow = uow
        
        self.event_dispatcher = event_dispatcher

    def execute(self, command: AnularCompraCommand) -> CompraDTO:
        purchase = self.repository.get_by_id(command.purchase_id)
        if purchase is None:
            raise CompraNoEncontradaException(command.purchase_id)

        now = datetime.now(timezone.utc)
        purchase.annul(timestamp=now, voided_by=command.voided_by, void_reason=command.void_reason)

        try:
            with self.uow:
                updated_purchase = self.repository.update(purchase)

                # Despachar eventos acumulados en el agregado
                for event in purchase.eventos:
                    if self.event_dispatcher:
                        self.event_dispatcher.dispatch(event)
                purchase.limpiar_eventos()
            
            return CompraDTOMapper.to_dto(updated_purchase)
        except Exception as e:
            raise e
