from datetime import datetime, timezone
from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.domain.exceptions.credito_no_encontrado_exception import CreditoNoEncontradoException
from app.modules.credito.application.ports.unit_of_work import UnitOfWork
from app.modules.credito.application.commands.registrar_cargo_command import RegistrarCargoCreditoCommand
from app.modules.credito.application.dto.credito_dto import CreditoDTO
from app.modules.credito.application.dto.credito_dto_mapper import CreditoDTOMapper
from app.common.event_dispatcher import EventDispatcher

class RegistrarCargoCreditoUseCase:
    def __init__(
        self,
        repository: CreditoRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: RegistrarCargoCreditoCommand) -> CreditoDTO:
        credito = self.repository.get_by_client_id(command.company_id, command.client_id)
        if credito is None:
            raise CreditoNoEncontradoException(command.client_id)

        now = datetime.now(timezone.utc)
        credito.add_debt(command.amount, reference_id=command.reference_id, timestamp=now)

        with self.uow:
            updated_credit = self.repository.update(credito)
            # Dispatch accumulated events
            for event in credito.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            credito.limpiar_eventos()

        return CreditoDTOMapper.to_dto(updated_credit)
