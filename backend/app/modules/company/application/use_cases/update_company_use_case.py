from uuid import UUID

from app.modules.company.domain.entities.company import Company
from app.modules.company.domain.repositories.company_repository import CompanyRepository
from app.modules.company.domain.exceptions.company_not_found_exception import (
    CompanyNotFoundException,
)
from app.common.exceptions import ValidationException


class UpdateCompanyUseCase:
    """
    Application use case responsible for updating an existing company.
    """

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def execute(
        self,
        company_id: UUID,
        updates: dict[str, object],
    ) -> Company:

        # Validar que existan campos para actualizar
        if not updates:
            raise ValidationException(
                "No se enviaron campos para actualizar."
            )

        # Buscar la empresa
        company = self.repository.get_by_id(company_id)

        if company is None:
            raise CompanyNotFoundException(company_id)

        # Actualizar únicamente los campos enviados
        company.update_profile(
            business_name=updates.get("business_name", company.business_name),
            trade_name=updates.get("trade_name", company.trade_name),
            email=updates.get("email", company.email),
            phone=updates.get("phone", company.phone),
            currency=updates.get("currency", company.currency),
            timezone=updates.get("timezone", company.timezone),
            status=updates.get("status", company.status),
        )

        # Guardar cambios
        updated_company = self.repository.update(company)

        return updated_company