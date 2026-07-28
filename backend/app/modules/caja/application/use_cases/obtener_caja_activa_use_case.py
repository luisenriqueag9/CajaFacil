from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.domain.exceptions import SesionCajaNotFoundException
from app.modules.caja.application.queries.obtener_sesion_query import ObtenerSesionQuery
from app.modules.caja.application.dto.sesion_caja_dto import SesionCajaDTO
from app.modules.caja.application.dto.sesion_caja_dto_mapper import SesionCajaDTOMapper

class ObtenerSesionUseCase:
    def __init__(self, repository: SesionCajaRepository):
        self.repository = repository

    def execute(self, query: ObtenerSesionQuery) -> SesionCajaDTO:
        sesion = self.repository.get_by_id(query.sesion_id)
        if sesion is None:
            raise SesionCajaNotFoundException(query.sesion_id)
        return SesionCajaDTOMapper.to_dto(sesion)
