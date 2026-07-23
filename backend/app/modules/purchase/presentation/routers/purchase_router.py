import uuid
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, Query

from app.common.presentation.responses import ApiResponse
from app.modules.purchase.domain.entities.purchase import Purchase
from app.modules.purchase.presentation.dependencies.purchase_dependencies import (
    get_register_purchase_use_case,
    get_annul_purchase_use_case,
    get_get_purchase_by_id_use_case,
    get_list_purchases_use_case,
)
from app.modules.purchase.presentation.dto import (
    PurchaseCreateRequest,
    PurchaseResponse,
)
from app.modules.purchase.application.use_cases import (
    RegisterPurchaseUseCase,
    AnnulPurchaseUseCase,
    GetPurchaseByIdUseCase,
    ListPurchasesUseCase,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ApiResponse[PurchaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def register_purchase(
    request: PurchaseCreateRequest,
    use_case: RegisterPurchaseUseCase = Depends(get_register_purchase_use_case),
) -> ApiResponse[PurchaseResponse]:
    """
    Registrar y confirmar una nueva compra de mercadería.
    """
    purchase_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    
    # Map detail request items to list of dict for register factory
    items_payload = [
        {
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_cost": item.unit_cost
        }
        for item in request.items
    ]

    purchase_entity = Purchase.register(
        id=purchase_id,
        company_id=request.company_id,
        supplier_id=request.supplier_id,
        invoice_number=request.invoice_number.strip(),
        payment_condition=request.payment_condition.strip().upper(),
        issue_date=request.issue_date,
        created_at=now,
        updated_at=now,
        items_payload=items_payload
    )

    created_purchase = use_case.execute(purchase_entity)
    purchase_response = PurchaseResponse.model_validate(created_purchase)

    return ApiResponse(
        success=True,
        message="Compra registrada y confirmada correctamente.",
        data=purchase_response,
    )

@router.get(
    "/",
    response_model=ApiResponse[list[PurchaseResponse]],
    status_code=status.HTTP_200_OK,
)
def list_purchases(
    company_id: UUID = Query(..., description="ID de la empresa obligatoria para listar sus compras"),
    status_filter: str | None = Query(None, alias="status", description="Filtrar por estado (BORRADOR/CONFIRMADA/ANULADA)"),
    supplier_id: UUID | None = Query(None, description="Filtrar por proveedor específico"),
    use_case: ListPurchasesUseCase = Depends(get_list_purchases_use_case),
) -> ApiResponse[list[PurchaseResponse]]:
    """
    Obtener la lista de compras del negocio filtrado por filtros.
    """
    purchases = use_case.execute(
        company_id=company_id, 
        status=status_filter, 
        supplier_id=supplier_id
    )
    purchase_responses = [PurchaseResponse.model_validate(p) for p in purchases]

    return ApiResponse(
        success=True,
        message="Compras obtenidas correctamente.",
        data=purchase_responses,
    )

@router.get(
    "/{purchase_id}",
    response_model=ApiResponse[PurchaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_purchase_by_id(
    purchase_id: UUID,
    use_case: GetPurchaseByIdUseCase = Depends(get_get_purchase_by_id_use_case),
) -> ApiResponse[PurchaseResponse]:
    """
    Obtener los detalles de una compra por su UUID.
    """
    purchase = use_case.execute(purchase_id)
    purchase_response = PurchaseResponse.model_validate(purchase)

    return ApiResponse(
        success=True,
        message="Compra obtenida correctamente.",
        data=purchase_response,
    )

@router.patch(
    "/{purchase_id}/annul",
    response_model=ApiResponse[bool],
    status_code=status.HTTP_200_OK,
)
def annul_purchase(
    purchase_id: UUID,
    use_case: AnnulPurchaseUseCase = Depends(get_annul_purchase_use_case),
) -> ApiResponse[bool]:
    """
    Anular comercialmente una compra confirmada.
    """
    success = use_case.execute(purchase_id)
    return ApiResponse(
        success=success,
        message="Compra anulada correctamente.",
        data=success,
    )
