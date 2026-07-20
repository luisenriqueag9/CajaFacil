import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from app.common.presentation.responses import ApiResponse
from app.modules.company.presentation.dto import CompanyCreateRequest, CompanyResponse
from app.modules.company.domain.entities.company import Company
from app.modules.company.application.use_cases.create_company_use_case import CreateCompanyUseCase
from app.modules.company.presentation.dependencies.company_dependencies import get_create_company_use_case
from app.modules.company.domain.exceptions import CompanyAlreadyExistsException, InvalidCompanyException

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=ApiResponse[CompanyResponse], status_code=status.HTTP_201_CREATED)
def create_company(
    request: CompanyCreateRequest,
    use_case: CreateCompanyUseCase = Depends(get_create_company_use_case)
) -> ApiResponse[CompanyResponse]:
    """
    Register a new Company in the system.
    Receives request DTO, maps to Domain entity, executes Use Case, and returns ApiResponse.
    """
    try:
        # Generate new identity and timestamps for the domain entity
        company_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        
        # Map CreateRequest DTO to Domain Entity
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
            updated_at=now
        )
        
        # Execute pure business logic Use Case
        created_company = use_case.execute(company_entity)
        
        # Map resultant Domain Entity to Response DTO
        company_response = CompanyResponse.model_validate(created_company)
        
        # Return standardized API response
        return ApiResponse(
            success=True,
            message="Company created successfully",
            data=company_response
        )
        
    except CompanyAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidCompanyException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
