from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria

class TaxConfigurationLookup(ABC):
    """
    Interface definition (Port) allowing external Bounded Contexts (Ventas, Compras)
    to query active tax configurations in a decoupled manner.
    """
    @abstractmethod
    def get_active_config(self, company_id: UUID) -> Optional[ConfiguracionTributaria]:
        pass
```,Description:
