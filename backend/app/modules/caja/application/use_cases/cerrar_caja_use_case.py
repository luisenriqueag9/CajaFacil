from datetime import datetime, timezone
from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.domain.exceptions import SesionCajaNotFoundException
from app.modules.caja.application.ports.unit_of_work import UnitOfWork
from app.modules.caja.application.commands.cerrar_sesion_command import CerrarSesionCommand
from app.modules.caja.application.dto.sesion_caja_dto import SesionCajaDTO
from app.modules.caja.application.dto.sesion_caja_dto_mapper import SesionCajaDTOMapper
from app.common.event_dispatcher import EventDispatcher

class CerrarSesionUseCase:
    def __init__(
        self,
        repository: SesionCajaRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: CerrarSesionCommand) -> SesionCajaDTO:
        sesion = self.repository.get_by_id(command.sesion_id)
        if sesion is None:
            raise SesionCajaNotFoundException(command.sesion_id)

        now = datetime.now(timezone.utc)
        sesion.cerrar(closed_at=now)

        with self.uow:
            updated_sesion = self.repository.update(sesion)
            # Dispatch events
            for event in sesion.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            sesion.limpiar_eventos()

        return SesionCajaDTOMapper.to_dto(updated_sesion)
