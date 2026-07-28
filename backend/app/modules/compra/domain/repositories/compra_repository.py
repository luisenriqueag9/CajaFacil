from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.compra.domain.aggregates.compra import Compra

class CompraRepository(ABC):

    @abstractmethod
    def create(self, compra: Compra) -> Compra:
        """Persiste una nueva compra."""
        pass

    @abstractmethod
    def get_by_id(self, purchase_id: UUID) -> Compra | None:
        """Obtiene una compra por su ID unico."""
        pass

    @abstractmethod
    def get_by_invoice_number(
        self, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: str
    ) -> Compra | None:
        """Obtiene una compra por su numero de factura y proveedor en una empresa."""
        pass

    @abstractmethod
    def get_all(
        self, 
        company_id: UUID, 
        status: str | None = None, 
        supplier_id: UUID | None = None
    ) -> list[Compra]:
        """Obtiene todas las compras de una empresa, con filtros opcionales."""
        pass

    @abstractmethod
    def update(self, compra: Compra) -> Compra:
        """Actualiza una compra existente."""
        pass
