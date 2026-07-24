from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.inventario.domain.entities.existencia import ExistenciaProducto

class ExistenciaRepository(ABC):
    @abstractmethod
    def save(self, existencia: ExistenciaProducto) -> ExistenciaProducto:
        """
        Persists a product stock state.
        Must NOT call db.commit() automatically.
        """
        pass

    @abstractmethod
    def get_by_product_id(self, company_id: UUID, product_id: UUID) -> Optional[ExistenciaProducto]:
        """
        Retrieves the stock state of a specific product for a company tenant.
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[ExistenciaProducto]:
        """
        Lists stock balances using tenant isolation.
        """
        pass
