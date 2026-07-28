from typing import List
from app.modules.caja.domain.repositories.sesion_caja_repository import SesionCajaRepository
from app.modules.caja.application.queries.listar_sesiones_query import ListarSesionesQuery
from app.modules.caja.application.dto.sesion_caja_dto import SesionCajaDTO
from app.modules.caja.application.dto.sesion_caja_dto_mapper import SesionCajaDTOMapper

class ListarSesionesUseCase:
    def __init__(self, repository: SesionCajaRepository):
        self.repository = repository

    def execute(self, query: ListarSesionesQuery) -> List[SesionCajaDTO]:
        sesiones = self.repository.get_all(company_id=query.company_id, status=query.status)
        return [SesionCajaDTOMapper.to_dto(s) for s in sesiones]
