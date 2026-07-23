from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.caja.domain.entities.caja import Caja

class CajaRepository(ABC):
    @abstractmethod
    def save(self, caja: Caja) -> Caja:
        """
        Persists a Caja session and its internal entities.
        Must NOT call db.commit() automatically.
        """
        pass

    @abstractmethod
    def get_by_id(self, caja_id: UUID) -> Optional[Caja]:
        """
        Retrieves a box session by ID.
        """
        pass

    @abstractmethod
    def get_active_by_user(self, company_id: UUID, user_id: UUID) -> Optional[Caja]:
        """
        Retrieves the active open box session for a user.
        Used to enforce custody invariants.
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[Caja]:
        """
        Queries box sessions applying tenant isolation and criteria filters.
        """
        pass
