from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

class AbrirCajaRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID of the cashier user")
    opening_balance: Decimal = Field(..., description="Fondo inicial de apertura en efectivo")


class RegistrarMovimientoCajaRequest(BaseModel):
    type: str = Field(..., description="INGRESO, EGRESO")
    amount: Decimal = Field(..., description="Amount transacted")
    payment_method: str = Field(..., description="EFECTIVO, TARJETA, TRANSFERENCIA, CREDITO")
    concept: str = Field(..., description="VENTA, COMPRA, RETIRO, GASTO, ABONO_CREDITO")
    origin_document_id: UUID | None = Field(None, description="Optional UUID of the original transaction document")


class RegistrarArqueoCajaRequest(BaseModel):
    physical_amount: Decimal = Field(..., description="Total physical cash counted in box drawer")
    supervisor_id: UUID | None = Field(None, description="Optional UUID of supervisor authorizing count discrepancy")


class CerrarCajaRequest(BaseModel):
    physical_amount: Decimal = Field(..., description="Final cash counted in drawer at shift closure")
    supervisor_id: UUID | None = Field(None, description="Optional UUID of supervisor authorizing closure discrepancy")
