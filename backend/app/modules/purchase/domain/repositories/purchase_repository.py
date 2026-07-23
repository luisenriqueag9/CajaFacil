from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.purchase.domain.entities.purchase import Purchase

class PurchaseRepository(ABC):

    @abstractmethod
    def create(self, purchase: Purchase) -> Purchase:
        """Persist a new purchase in storage."""
        pass

    @abstractmethod
    def get_by_id(self, purchase_id: UUID) -> Purchase | None:
        """Retrieve a purchase by its unique identifier."""
        pass

    @abstractmethod
    def get_by_invoice_number(
        self, 
        company_id: UUID, 
        supplier_id: UUID, 
        invoice_number: str
    ) -> Purchase | None:
        """Retrieve a purchase by its invoice number and supplier within a company context."""
        pass

    @abstractmethod
    def get_all(
        self, 
        company_id: UUID, 
        status: str | None = None, 
        supplier_id: UUID | None = None
    ) -> list[Purchase]:
        """Retrieve all purchases belonging to the company, optionally filtering by status and supplier."""
        pass

    @abstractmethod
    def update(self, purchase: Purchase) -> Purchase:
        """Update an existing purchase's state in storage."""
        pass
