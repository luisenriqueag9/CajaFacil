from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.modules.caja.domain.entities.caja import Caja

class CajaRepository(ABC):
    @abstractmethod
    def create(self, caja: Caja) -> Caja:
        """Crea un nuevo recurso de caja fisica."""
        pass

    @abstractmethod
    def get_by_id(self, caja_id: UUID) -> Caja | None:
        """Recupera una caja fisica por ID."""
        pass

    @abstractmethod
    def get_all(self, company_id: UUID) -> List[Caja]:
        """Obtiene todas las cajas fisicas de la empresa."""
        pass
