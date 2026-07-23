from uuid import UUID
from app.modules.venta.domain.entities.venta import Venta
from app.modules.venta.domain.repositories.venta_repository import VentaRepository
from app.modules.venta.domain.exceptions import VentaNotFoundException

class GetVentaByIdUseCase:
    """
    Application Use Case to query a single sale by ID.
    """
    def __init__(self, repository: VentaRepository):
        self.repository = repository

    def execute(self, company_id: UUID, venta_id: UUID) -> Venta:
        venta = self.repository.get_by_id(venta_id)
        
        # Enforce multi-tenant isolation
        if venta is None or venta.company_id != company_id:
            raise VentaNotFoundException(venta_id)
            
        return venta
