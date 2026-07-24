import uuid
from typing import List, Dict, Any
from app.modules.tributacion.domain.entities.configuracion import DesgloseImpuesto
from app.modules.tributacion.domain.repositories.configuracion_repository import ConfiguracionTributariaRepository
from app.modules.tributacion.domain.services.motor_tributario import MotorTributario

class CalcularImpuestoTransaccionUseCase:
    """
    Application Use Case acting as a wrapper/coordinator to execute tax calculations
    for items under a specific company tenant context.
    """
    def __init__(self, repository: ConfiguracionTributariaRepository):
        self.repository = repository
        self.motor = MotorTributario()

    def execute(self, company_id: uuid.UUID, items: List[Dict[str, Any]]) -> List[DesgloseImpuesto]:
        config = self.repository.get_active_by_company(company_id)
        return self.motor.calcular(items, config)
