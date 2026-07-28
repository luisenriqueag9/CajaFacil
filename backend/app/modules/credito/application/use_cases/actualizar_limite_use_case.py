from datetime import datetime, timezone
from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.domain.exceptions.credito_no_encontrado_exception import CreditoNoEncontradoException
from app.modules.credito.application.ports.unit_of_work import UnitOfWork
from app.modules.credito.application.commands.actualizar_limite_command import ActualizarLimiteCreditoCommand
from app.modules.credito.application.dto.credito_dto import CreditoDTO
from app.modules.credito.application.dto.credito_dto_mapper import CreditoDTOMapper
from app.common.event_dispatcher import EventDispatcher

class ActualizarLimiteCreditoUseCase:
    def __init__(
        self,
        repository: CreditoRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: ActualizarLimiteCreditoCommand) -> CreditoDTO:
        credito = self.repository.get_by_id(command.credit_id)
        if credito is None:
            raise CreditoNoEncontradoException(command.credit_id)

        now = datetime.now(timezone.utc)
        credito.update_limit(command.new_limit, timestamp=now)

        with self.uow:
            updated_credit = self.repository.update(credito)
            # Dispatch accumulated events
            for event in credito.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            credito.limpiar_eventos()

        return CreditoDTOMapper.to_dto(updated_credit)
