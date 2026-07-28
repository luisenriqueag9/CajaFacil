from typing import List
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.application.queries.listar_clientes_query import ListarClientesQuery
from app.modules.cliente.application.dto.cliente_dto import ClienteDTO
from app.modules.cliente.application.dto.cliente_dto_mapper import ClienteDTOMapper

class ListarClientesUseCase:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def execute(self, query: ListarClientesQuery) -> List[ClienteDTO]:
        clientes = self.repository.get_all(company_id=query.company_id, status=query.status)
        return [ClienteDTOMapper.to_dto(c) for c in clientes]
