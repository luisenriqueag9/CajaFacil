from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.domain.exceptions.compra_no_encontrada_exception import CompraNoEncontradaException
from app.modules.compra.application.queries.obtener_compra_query import ObtenerCompraQuery
from app.modules.compra.application.dto.compra_dto import CompraDTO
from app.modules.compra.application.dto.compra_dto_mapper import CompraDTOMapper

class ObtenerCompraUseCase:
    """
    Caso de uso para obtener una unica compra por su identificador unico.
    """
    def __init__(self, repository: CompraRepository):
        self.repository = repository

    def execute(self, query: ObtenerCompraQuery) -> CompraDTO:
        purchase = self.repository.get_by_id(query.purchase_id)
        if purchase is None:
            raise CompraNoEncontradaException(query.purchase_id)
        return CompraDTOMapper.to_dto(purchase)
