import uuid
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status

from app.common.presentation.responses import ApiResponse

from app.modules.company.application.use_cases.create_company_use_case import (
    CreateCompanyUseCase,
)
from app.modules.company.application.use_cases.get_company_by_id_use_case import (
    GetCompanyByIdUseCase,
)
from app.modules.company.application.use_cases.get_all_companies_use_case import (
    GetAllCompaniesUseCase,
)
from app.modules.company.application.use_cases.update_company_use_case import (
    UpdateCompanyUseCase,
)

from app.modules.company.domain.entities.company import Company

from app.modules.company.presentation.dependencies.company_dependencies import (
    get_create_company_use_case,
    get_company_by_id_use_case,
    get_all_companies_use_case,
    get_update_company_use_case,
)

from app.modules.company.presentation.dto import (
    CompanyCreateRequest,
    CompanyUpdateRequest,
    CompanyResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ApiResponse[CompanyResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    request: CompanyCreateRequest,
    use_case: CreateCompanyUseCase = Depends(get_create_company_use_case),
) -> ApiResponse[CompanyResponse]:
    """
    Crear una nueva empresa.
    """

    company_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    company_entity = Company(
        id=company_id,
        business_name=request.business_name,
        trade_name=request.trade_name,
        tax_id=request.tax_id,
        email=request.email,
        phone=request.phone,
        country=request.country,
        currency=request.currency,
        timezone=request.timezone,
        status=request.status,
        created_at=now,
        updated_at=now,
    )

    created_company = use_case.execute(company_entity)

    company_response = CompanyResponse.model_validate(created_company)

    return ApiResponse(
        success=True,
        message="Empresa creada correctamente.",
        data=company_response,
    )


@router.get(
    "/",
    response_model=ApiResponse[list[CompanyResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_companies(
    use_case: GetAllCompaniesUseCase = Depends(get_all_companies_use_case),
) -> ApiResponse[list[CompanyResponse]]:
    """
    Obtener todas las empresas registradas.
    """

    companies = use_case.execute()

    company_responses = [
        CompanyResponse.model_validate(company)
        for company in companies
    ]

    return ApiResponse(
        success=True,
        message="Empresas obtenidas correctamente.",
        data=company_responses,
    )


@router.get(
    "/{company_id}",
    response_model=ApiResponse[CompanyResponse],
    status_code=status.HTTP_200_OK,
)
def get_company_by_id(
    company_id: UUID,
    use_case: GetCompanyByIdUseCase = Depends(get_company_by_id_use_case),
) -> ApiResponse[CompanyResponse]:
    """
    Obtener una empresa por su identificador.
    """

    company = use_case.execute(company_id)

    company_response = CompanyResponse.model_validate(company)

    return ApiResponse(
        success=True,
        message="Empresa obtenida correctamente.",
        data=company_response,
    )


@router.put(
    "/{company_id}",
    response_model=ApiResponse[CompanyResponse],
    status_code=status.HTTP_200_OK,
)
def update_company(
    company_id: UUID,
    request: CompanyUpdateRequest,
    use_case: UpdateCompanyUseCase = Depends(get_update_company_use_case),
) -> ApiResponse[CompanyResponse]:
    """
    Actualizar una empresa existente.
    """

    updated_company = use_case.execute(
        company_id=company_id,
        updates=request.model_dump(exclude_unset=True),
    )

    company_response = CompanyResponse.model_validate(updated_company)

    return ApiResponse(
        success=True,
        message="Empresa actualizada correctamente.",
        data=company_response,
    )