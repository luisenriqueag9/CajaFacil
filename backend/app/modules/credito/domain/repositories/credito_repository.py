from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.modules.credito.domain.aggregates.credito import Credito

class CreditoRepository(ABC):
    @abstractmethod
    def create(self, credito: Credito) -> Credito:
        """Persiste una nueva cuenta de credito."""
        pass

    @abstractmethod
    def get_by_id(self, credit_id: UUID) -> Credito | None:
        """Recupera una cuenta de credito por su ID."""
        pass

    @abstractmethod
    def get_by_client_id(self, company_id: UUID, client_id: UUID) -> Credito | None:
        """Recupera la cuenta de credito de un cliente dentro de una empresa."""
        pass

    @abstractmethod
    def get_all(self, company_id: UUID, status: str | None = None) -> List[Credito]:
        """Obtiene todas las cuentas de credito de una empresa."""
        pass

    @abstractmethod
    def update(self, credito: Credito) -> Credito:
        """Actualiza una cuenta de credito existente."""
        pass
