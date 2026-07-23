from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.inventario.domain.entities.movimiento import MovimientoInventario

class MovimientoInventarioRepository(ABC):
    @abstractmethod
    def save(self, movimiento: MovimientoInventario) -> MovimientoInventario:
        """
        Persists a MovimientoInventario.
        Must NOT call db.commit() automatically.
        """
        pass

    @abstractmethod
    def get_by_id(self, movimiento_id: UUID) -> Optional[MovimientoInventario]:
        """
        Retrieves a movement by its ID.
        """
        pass

    @abstractmethod
    def get_by_product_id(self, company_id: UUID, product_id: UUID) -> List[MovimientoInventario]:
        """
        Retrieves all movements associated with a product (Kardex).
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[MovimientoInventario]:
        """
        Performs advanced search over movements applying tenant isolation and criteria.
        """
        pass
