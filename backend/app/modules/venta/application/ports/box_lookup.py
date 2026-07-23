from abc import ABC, abstractmethod
from uuid import UUID

class BoxLookup(ABC):
    @abstractmethod
    def is_open_and_active(self, company_id: UUID, box_id: UUID) -> bool:
        """Verify that a cash register box is open and active for operations."""
        pass
