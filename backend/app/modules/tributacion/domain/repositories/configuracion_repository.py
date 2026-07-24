from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria

class ConfiguracionTributariaRepository(ABC):
    @abstractmethod
    def save(self, config: ConfiguracionTributaria) -> ConfiguracionTributaria:
        """
        Persists a tax configuration session and its internal rates.
        Must NOT call db.commit() automatically.
        """
        pass

    @abstractmethod
    def get_by_id(self, config_id: UUID) -> Optional[ConfiguracionTributaria]:
        """
        Retrieves a tax configuration by ID.
        """
        pass

    @abstractmethod
    def get_active_by_company(self, company_id: UUID) -> Optional[ConfiguracionTributaria]:
        """
        Retrieves the currently active tax configuration for a company.
        Used to calculate tax in transactions.
        """
        pass

    @abstractmethod
    def search(self, company_id: UUID, filters: dict) -> List[ConfiguracionTributaria]:
        """
        Queries configurations applying tenant isolation and criteria filters.
        """
        pass
