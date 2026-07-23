import uuid
from typing import Optional
from app.modules.caja.domain.entities.caja import Caja
from app.modules.caja.domain.repositories.caja_repository import CajaRepository

class ObtenerCajaActivaUseCase:
    """
    Application Use Case to query the current active (open) box session for a user.
    """
    def __init__(self, repository: CajaRepository):
        self.repository = repository

    def execute(self, company_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Caja]:
        return self.repository.get_active_by_user(company_id, user_id)
