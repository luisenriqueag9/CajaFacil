from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.modules.caja.domain.aggregates.sesion_caja import SesionCaja

class SesionCajaRepository(ABC):
    @abstractmethod
    def create(self, sesion: SesionCaja) -> SesionCaja:
        """Persiste una nueva sesion de caja."""
        pass

    @abstractmethod
    def get_by_id(self, sesion_id: UUID) -> SesionCaja | None:
        """Recupera una sesion de caja por su ID."""
        pass

    @abstractmethod
    def get_active_by_user(self, company_id: UUID, user_id: UUID) -> SesionCaja | None:
        """Recupera la sesion activa del usuario en la empresa."""
        pass

    @abstractmethod
    def get_active_by_caja(self, company_id: UUID, caja_id: UUID) -> SesionCaja | None:
        """Recupera la sesion activa asignada a una caja fisica."""
        pass

    @abstractmethod
    def get_all(self, company_id: UUID, status: str | None = None) -> List[SesionCaja]:
        """Obtiene todas las sesiones de la empresa."""
        pass

    @abstractmethod
    def update(self, sesion: SesionCaja) -> SesionCaja:
        """Actualiza una sesion de caja existente (agrega movimientos/arqueos)."""
        pass
