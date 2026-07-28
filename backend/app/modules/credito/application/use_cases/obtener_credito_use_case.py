from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.domain.exceptions.credito_no_encontrado_exception import CreditoNoEncontradoException
from app.modules.credito.application.queries.obtener_credito_query import ObtenerCreditoQuery
from app.modules.credito.application.dto.credito_dto import CreditoDTO
from app.modules.credito.application.dto.credito_dto_mapper import CreditoDTOMapper

class ObtenerCreditoUseCase:
    def __init__(self, repository: CreditoRepository):
        self.repository = repository

    def execute(self, query: ObtenerCreditoQuery) -> CreditoDTO:
        credito = self.repository.get_by_id(query.credit_id)
        if credito is None:
            raise CreditoNoEncontradoException(query.credit_id)
        return CreditoDTOMapper.to_dto(credito)
