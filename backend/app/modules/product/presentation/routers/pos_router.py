from uuid import UUID
from fastapi import APIRouter, Depends, Query, Header, status

from app.common.presentation.responses import ApiResponse
from app.modules.product.presentation.dependencies.product_dependencies import get_list_products_use_case
from app.modules.product.application.use_cases import ListProductsUseCase
from app.modules.product.presentation.dto.pos_product_search_response import POSProductSearchResponse

router = APIRouter()

def get_pos_company_context(x_company_id: str | None = Header(None, alias="X-Company-ID")) -> UUID:
    """
    Extracts the tenant company ID from the X-Company-ID request header.
    Falls back to a default development UUID if not provided by the UI.
    """
    if x_company_id:
        try:
            return UUID(x_company_id)
        except ValueError:
            pass
    # Fallback to the default company in the seeded database
    return UUID("dc555b36-ede8-432c-a8b9-a31294c8308a")

@router.get(
    "/search-products",
    response_model=ApiResponse[list[POSProductSearchResponse]],
    status_code=status.HTTP_200_OK,
)
def search_products(
    search: str | None = Query(None, description="Term to search by barcode, internal code or name"),
    limit: int = Query(50, ge=1, le=1000, description="Limit of products to retrieve"),
    company_id: UUID = Depends(get_pos_company_context),
    use_case: ListProductsUseCase = Depends(get_list_products_use_case),
) -> ApiResponse[list[POSProductSearchResponse]]:
    """
    POS specialized endpoint that returns a light, decoupled projection of products for search autocompletion.
    """
    # Enforce maximum safety limit of 50 on the server
    clamped_limit = min(limit, 50)

    # Re-use existing ListProductsUseCase
    products = use_case.execute(
        company_id=company_id,
        search=search,
        limit=clamped_limit,
        status="ACTIVO",  # POS only searches active products
    )

    # Map to POSProductSearchResponse projection
    response_data = [
        POSProductSearchResponse(
            id=p.id,
            code=p.barcode if p.barcode else p.internal_code,
            name=p.name,
            price=float(p.price)
        )
        for p in products
    ]

    return ApiResponse(
        success=True,
        message="POS products matching query fetched successfully.",
        data=response_data
    )
