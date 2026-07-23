from uuid import UUID
from app.modules.venta.domain.entities.venta import Venta
from app.modules.venta.domain.repositories.venta_repository import VentaRepository

class ListSalesUseCase:
    """
    Application Use Case to list sales applying tenant isolation and criteria.
    """
    def __init__(self, repository: VentaRepository):
        self.repository = repository

    def execute(self, company_id: UUID, filters: dict) -> list[Venta]:
        return self.repository.search(company_id, filters)
