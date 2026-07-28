import uuid
from datetime import datetime, timezone
from app.modules.caja.domain.aggregates.sesion_caja import SesionCaja
from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.exceptions import (
    CajaNotFoundException,
    CajaYaAbiertaException
)
from app.modules.caja.application.ports.unit_of_work import UnitOfWork
from app.modules.caja.application.commands.abrir_sesion_command import AbrirSesionCommand
from app.modules.caja.application.dto.sesion_caja_dto import SesionCajaDTO
from app.modules.caja.application.dto.sesion_caja_dto_mapper import SesionCajaDTOMapper
from app.common.event_dispatcher import EventDispatcher

class AbrirSesionUseCase:
    def __init__(
        self,
        repository: SesionCajaRepository,
        caja_repository: CajaRepository,
        uow: UnitOfWork,
        event_dispatcher: EventDispatcher = None
    ):
        self.repository = repository
        self.caja_repository = caja_repository
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    def execute(self, command: AbrirSesionCommand) -> SesionCajaDTO:
        # Check physical register exists
        caja = self.caja_repository.get_by_id(command.caja_id)
        if caja is None:
            raise CajaNotFoundException(command.caja_id)

        # Check if user already has an active session
        active_user_session = self.repository.get_active_by_user(command.company_id, command.user_id)
        if active_user_session is not None:
            raise CajaYaAbiertaException(command.user_id)

        # Check if physical box is already in use by another session
        active_box_session = self.repository.get_active_by_caja(command.company_id, command.caja_id)
        if active_box_session is not None:
            raise CajaYaAbiertaException(active_box_session.user_id)

        sesion_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        sesion = SesionCaja.abrir(
            id=sesion_id,
            caja_id=command.caja_id,
            company_id=command.company_id,
            user_id=command.user_id,
            opening_balance=command.opening_balance,
            opened_at=now
        )

        with self.uow:
            created_sesion = self.repository.create(sesion)
            # Dispatch events
            for event in sesion.eventos:
                if self.event_dispatcher:
                    self.event_dispatcher.dispatch(event)
            sesion.limpiar_eventos()

        return SesionCajaDTOMapper.to_dto(created_sesion)
