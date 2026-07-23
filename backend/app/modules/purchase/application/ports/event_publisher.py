from abc import ABC, abstractmethod

class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: object) -> None:
        """Publish a domain or integration event to listeners."""
        pass
