from uuid import UUID
from typing import List
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario
from app.modules.inventario.domain.repositories.movimiento_repository import MovimientoInventarioRepository

class ListarMovimientosUseCase:
    """
    Application Use Case to fetch movements applying multi-tenant isolation and filters.
    """
    def __init__(self, repository: MovimientoInventarioRepository):
        self.repository = repository

    def execute(self, company_id: UUID, filters: dict) -> List[MovimientoInventario]:
        return self.repository.search(company_id, filters)
