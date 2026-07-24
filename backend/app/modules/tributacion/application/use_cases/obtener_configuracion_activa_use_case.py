import uuid
from typing import Optional
from app.modules.tributacion.domain.entities.configuracion import ConfiguracionTributaria
from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository

class ObtenerConfiguracionActivaUseCase:
    """
    Application Use Case to query the currently active tax configuration for a company.
    """
    def __init__(self, repository: ConfiguracionTributariaRepository):
        self.repository = repository

    def execute(self, company_id: uuid.UUID) -> Optional[ConfiguracionTributaria]:
        return self.repository.get_active_by_company(company_id)
