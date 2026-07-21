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
from app.modules.company.domain.entities.company import Company
from app.modules.company.presentation.dependencies.company_dependencies import (
    get_create_company_use_case,
    get_company_by_id_use_case,
    get_all_companies_use_case,
)
from app.modules.company.presentation.dto import (
    CompanyCreateRequest,
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
    Register a new Company in the system.
    Receives request DTO, maps to Domain entity, executes Use Case,
    and returns a standardized API response.
    """

    # Generate identity and timestamps
    company_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    # Map DTO -> Domain Entity
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

    # Execute business logic
    created_company = use_case.execute(company_entity)

    # Map Domain -> Response DTO
    company_response = CompanyResponse.model_validate(created_company)

    # Standardized response
    return ApiResponse(
        success=True,
        message="Company created successfully",
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
    Retrieve all registered companies.
    """

    # Execute business logic
    companies = use_case.execute()

    # Map Domain -> Response DTO
    company_responses = [
        CompanyResponse.model_validate(company)
        for company in companies
    ]

    # Standardized response
    return ApiResponse(
        success=True,
        message="Companies retrieved successfully",
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
    Retrieve a company by its unique identifier.
    """

    # Execute business logic
    company = use_case.execute(company_id)

    # Map Domain -> Response DTO
    company_response = CompanyResponse.model_validate(company)

    # Standardized response
    return ApiResponse(
        success=True,
        message="Company retrieved successfully",
        data=company_response,
    )