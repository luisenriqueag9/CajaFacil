from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> "UnitOfWork":
        """Inicia el contexto transaccional encapsulado."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Finaliza el contexto transaccional, revirtiendo ante excepciones."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Confirma los cambios."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Revierte los cambios."""
        pass
