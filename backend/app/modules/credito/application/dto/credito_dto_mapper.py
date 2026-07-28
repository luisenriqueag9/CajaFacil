from app.modules.credito.application.dto.credito_dto import CreditoDTO
from app.modules.credito.domain.aggregates.credito import Credito

class CreditoDTOMapper:
    @staticmethod
    def to_dto(credito: Credito) -> CreditoDTO:
        return CreditoDTO(
            id=credito.id,
            company_id=credito.company_id,
            client_id=credito.client_id,
            credit_limit=credito.credit_limit.monto,
            balance=credito.balance.monto,
            status=credito.status.valor,
            created_at=credito.created_at,
            updated_at=credito.updated_at
        )
