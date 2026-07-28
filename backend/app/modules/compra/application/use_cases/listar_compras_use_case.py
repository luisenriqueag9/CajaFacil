from typing import List
from app.modules.compra.domain.repositories.compra_repository import CompraRepository
from app.modules.compra.application.queries.listar_compras_query import ListarComprasQuery
from app.modules.compra.application.dto.compra_dto import CompraDTO
from app.modules.compra.application.dto.compra_dto_mapper import CompraDTOMapper

class ListarComprasUseCase:
    """
    Caso de uso para listar compras de una empresa con filtros de estado y proveedor.
    """
    def __init__(self, repository: CompraRepository):
        self.repository = repository

    def execute(self, query: ListarComprasQuery) -> List[CompraDTO]:
        purchases = self.repository.get_all(
            company_id=query.company_id, 
            status=query.status, 
            supplier_id=query.supplier_id
        )
        return [CompraDTOMapper.to_dto(p) for p in purchases]
