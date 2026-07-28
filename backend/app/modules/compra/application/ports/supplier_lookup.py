from abc import ABC, abstractmethod
from uuid import UUID

class SupplierLookup(ABC):
    @abstractmethod
    def exists_and_active(self, company_id: UUID, supplier_id: UUID) -> bool:
        """Verify that a supplier exists and is active under the company."""
        pass
