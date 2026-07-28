from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.domain.exceptions.cliente_no_encontrado_exception import ClienteNoEncontradoException
from app.modules.cliente.application.queries.obtener_cliente_query import ObtenerClienteQuery
from app.modules.cliente.application.dto.cliente_dto import ClienteDTO
from app.modules.cliente.application.dto.cliente_dto_mapper import ClienteDTOMapper

class ObtenerClienteUseCase:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def execute(self, query: ObtenerClienteQuery) -> ClienteDTO:
        cliente = self.repository.get_by_id(query.client_id)
        if cliente is None:
            raise ClienteNoEncontradoException(query.client_id)
        return ClienteDTOMapper.to_dto(cliente)
