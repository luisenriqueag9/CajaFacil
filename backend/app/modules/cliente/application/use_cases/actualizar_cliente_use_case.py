from datetime import datetime, timezone
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.exceptions.cliente_no_encontrado_exception import ClienteNoEncontradoException
from app.modules.cliente.domain.exceptions.cliente_ya_existe_exception import ClienteYaExisteException
from app.modules.cliente.application.ports.unit_of_work import UnitOfWork
from app.modules.cliente.application.commands.actualizar_cliente_command import ActualizarClienteCommand
from app.modules.cliente.application.dto.cliente_dto import ClienteDTO
from app.modules.cliente.application.dto.cliente_dto_mapper import ClienteDTOMapper
from app.common.event_dispatcher import EventDispatcher

class ActualizarClienteUseCase:
    def __init__(
        self,
        repository: ClienteRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: ActualizarClienteCommand) -> ClienteDTO:
        cliente = self.repository.get_by_id(command.client_id)
        if cliente is None:
            raise ClienteNoEncontradoException(command.client_id)

        # Check uniqueness of tax_id if updated
        if command.tax_id and command.tax_id != cliente.tax_id:
            existing = self.repository.get_by_tax_id(cliente.company_id, command.tax_id)
            if existing is not None and existing.id != cliente.id:
                raise ClienteYaExisteException(command.tax_id, cliente.company_id)

        now = datetime.now(timezone.utc)
        cliente.update_profile(
            name=command.name,
            tax_id=command.tax_id,
            phone=command.phone,
            email=command.email,
            timestamp=now
        )

        with self.uow:
            updated_client = self.repository.update(cliente)
            # Dispatch accumulated events
            for event in cliente.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            cliente.limpiar_eventos()

        return ClienteDTOMapper.to_dto(updated_client)
