from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.venta.domain.entities.venta import Venta

class VentaRepository(ABC):
    
    @abstractmethod
    def save(self, venta: Venta) -> Venta:
        """
        Persists the aggregate complete (Venta, details and payments).
        Does NOT commit the database session directly to support unit of work.
        """
        pass
        
    @abstractmethod
    def get_by_id(self, venta_id: UUID) -> Optional[Venta]:
        """
        Retrieves the aggregate root with its details and payments.
        """
        pass
        
    @abstractmethod
    def get_by_invoice_number(self, company_id: UUID, invoice_number: str) -> Optional[Venta]:
        """
        Retrieves a Venta by its invoice number.
        """
        pass
        
    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[Venta]:
        """
        Searches for Ventas applying company isolation and filters.
        """
        pass
