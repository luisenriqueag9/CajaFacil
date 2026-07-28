from app.modules.cliente.application.dto.cliente_dto import ClienteDTO
from app.modules.cliente.domain.aggregates.cliente import Cliente

class ClienteDTOMapper:
    @staticmethod
    def to_dto(cliente: Cliente) -> ClienteDTO:
        return ClienteDTO(
            id=cliente.id,
            company_id=cliente.company_id,
            name=cliente.name.valor,
            tax_id=cliente.tax_id,
            phone=cliente.phone,
            email=cliente.email.valor if cliente.email.valor else None,
            status=cliente.status.valor,
            created_at=cliente.created_at,
            updated_at=cliente.updated_at
        )
