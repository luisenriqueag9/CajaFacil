import uuid
from datetime import datetime, timezone

from app.modules.credito.domain.aggregates.credito import Credito
from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.domain.exceptions.credito_ya_existe_exception import CreditoYaExisteException
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.exceptions.cliente_no_encontrado_exception import ClienteNoEncontradoException
from app.modules.credito.application.ports.unit_of_work import UnitOfWork
from app.modules.credito.application.commands.abrir_cuenta_command import AbrirCuentaCreditoCommand
from app.modules.credito.application.dto.credito_dto import CreditoDTO
from app.modules.credito.application.dto.credito_dto_mapper import CreditoDTOMapper
from app.common.event_dispatcher import EventDispatcher

class AbrirCuentaCreditoUseCase:
    def __init__(
        self,
        repository: CreditoRepository,
        cliente_repository: ClienteRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.cliente_repository = cliente_repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: AbrirCuentaCreditoCommand) -> CreditoDTO:
        # Validate that client exists
        client = self.cliente_repository.get_by_id(command.client_id)
        if client is None:
            raise ClienteNoEncontradoException(command.client_id)

        # Check uniqueness of credit account for client
        existing = self.repository.get_by_client_id(command.company_id, command.client_id)
        if existing is not None:
            raise CreditoYaExisteException(command.client_id, command.company_id)

        credit_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        credito = Credito.open_account(
            id=credit_id,
            company_id=command.company_id,
            client_id=command.client_id,
            credit_limit=command.credit_limit,
            created_at=now,
            updated_at=now
        )

        with self.uow:
            created_credit = self.repository.create(credito)
            # Dispatch accumulated events
            for event in credito.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            credito.limpiar_eventos()

        return CreditoDTOMapper.to_dto(created_credit)
