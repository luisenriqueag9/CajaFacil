from typing import List
from app.modules.credito.domain.repositories.credito_repository import CreditoRepository
from app.modules.credito.application.queries.listar_creditos_query import ListarCreditosQuery
from app.modules.credito.application.dto.credito_dto import CreditoDTO
from app.modules.credito.application.dto.credito_dto_mapper import CreditoDTOMapper

class ListarCreditosUseCase:
    def __init__(self, repository: CreditoRepository):
        self.repository = repository

    def execute(self, query: ListarCreditosQuery) -> List[CreditoDTO]:
        creditos = self.repository.get_all(company_id=query.company_id, status=query.status)
        return [CreditoDTOMapper.to_dto(c) for c in creditos]
