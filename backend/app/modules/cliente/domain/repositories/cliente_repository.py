from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.modules.cliente.domain.aggregates.cliente import Cliente

class ClienteRepository(ABC):
    @abstractmethod
    def create(self, cliente: Cliente) -> Cliente:
        """Persiste un nuevo cliente."""
        pass

    @abstractmethod
    def get_by_id(self, client_id: UUID) -> Cliente | None:
        """Recupera un cliente por su ID."""
        pass

    @abstractmethod
    def get_by_tax_id(self, company_id: UUID, tax_id: str) -> Cliente | None:
        """Recupera un cliente por su tax_id dentro de la empresa."""
        pass

    @abstractmethod
    def get_all(self, company_id: UUID, status: str | None = None) -> List[Cliente]:
        """Obtiene todos los clientes de una empresa con filtro de estado opcional."""
        pass

    @abstractmethod
    def update(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente existente."""
        pass
