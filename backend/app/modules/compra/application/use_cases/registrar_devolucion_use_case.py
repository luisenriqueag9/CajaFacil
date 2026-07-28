from datetime import datetime, timezone
from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.domain.exceptions.compra_no_encontrada_exception import CompraNoEncontradaException
from app.modules.compra.application.ports.unit_of_work import UnitOfWork
from app.modules.compra.application.commands.registrar_devolucion_command import RegistrarDevolucionProveedorCommand
from app.modules.compra.application.dto.compra_dto import CompraDTO
from app.modules.compra.application.dto.compra_dto_mapper import CompraDTOMapper
from app.common.event_dispatcher import EventDispatcher

class RegistrarDevolucionProveedorUseCase:
    """
    Caso de uso para registrar una devolucion al proveedor sobre una compra confirmada.
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

    def execute(self, command: RegistrarDevolucionProveedorCommand) -> CompraDTO:
        purchase = self.repository.get_by_id(command.purchase_id)
        if purchase is None:
            raise CompraNoEncontradaException(command.purchase_id)

        now = datetime.now(timezone.utc)
        items_payload = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            }
            for item in command.items
        ]

        purchase.devolver_proveedor(timestamp=now, items_returned=items_payload)

        try:
            with self.uow:
                updated_purchase = self.repository.update(purchase)

                # Despachar eventos de dominio acumulados en el agregado
                for event in purchase.eventos:
                    if self.event_dispatcher:
                        self.event_dispatcher.dispatch(event)
                purchase.limpiar_eventos()

            return CompraDTOMapper.to_dto(updated_purchase)
        except Exception as e:
            raise e
