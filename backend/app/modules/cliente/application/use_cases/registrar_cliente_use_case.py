import uuid
from datetime import datetime, timezone

from app.modules.cliente.domain.aggregates.cliente import Cliente
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.exceptions.cliente_ya_existe_exception import ClienteYaExisteException
from app.modules.cliente.application.ports.unit_of_work import UnitOfWork
from app.modules.cliente.application.commands.registrar_cliente_command import RegistrarClienteCommand
from app.modules.cliente.application.dto.cliente_dto import ClienteDTO
from app.modules.cliente.application.dto.cliente_dto_mapper import ClienteDTOMapper
from app.common.event_dispatcher import EventDispatcher

class RegistrarClienteUseCase:
    def __init__(
        self,
        repository: ClienteRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: RegistrarClienteCommand) -> ClienteDTO:
        # Check uniqueness of tax_id within the company context
        if command.tax_id:
            existing = self.repository.get_by_tax_id(command.company_id, command.tax_id)
            if existing is not None:
                raise ClienteYaExisteException(command.tax_id, command.company_id)

        client_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        cliente = Cliente.register(
            id=client_id,
            company_id=command.company_id,
            name=command.name,
            tax_id=command.tax_id,
            phone=command.phone,
            email=command.email,
            created_at=now,
            updated_at=now
        )

        with self.uow:
            created_client = self.repository.create(cliente)
            # Dispatch accumulated events
            for event in cliente.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            cliente.limpiar_eventos()

        return ClienteDTOMapper.to_dto(created_client)
