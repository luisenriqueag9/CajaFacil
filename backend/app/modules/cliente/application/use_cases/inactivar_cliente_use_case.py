from datetime import datetime, timezone
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.exceptions.cliente_no_encontrado_exception import ClienteNoEncontradoException
from app.modules.cliente.application.ports.unit_of_work import UnitOfWork
from app.modules.cliente.application.commands.inactivar_cliente_command import InactivarClienteCommand
from app.modules.cliente.application.dto.cliente_dto import ClienteDTO
from app.modules.cliente.application.dto.cliente_dto_mapper import ClienteDTOMapper
from app.common.event_dispatcher import EventDispatcher

class InactivarClienteUseCase:
    def __init__(
        self,
        repository: ClienteRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: InactivarClienteCommand) -> ClienteDTO:
        cliente = self.repository.get_by_id(command.client_id)
        if cliente is None:
            raise ClienteNoEncontradoException(command.client_id)

        now = datetime.now(timezone.utc)
        cliente.deactivate(timestamp=now)

        with self.uow:
            updated_client = self.repository.update(cliente)
            # Dispatch events
            for event in cliente.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            cliente.limpiar_eventos()

        return ClienteDTOMapper.to_dto(updated_client)
