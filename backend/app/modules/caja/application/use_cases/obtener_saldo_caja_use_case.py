import uuid
from decimal import Decimal
from typing import TypedDict
from app.modules.caja.domain.repositories.caja_repository import CajaRepository
from app.modules.caja.domain.exceptions import CajaNotFoundException

class SaldoCajaBreakdown(TypedDict):
    expected_cash: Decimal
    expected_card: Decimal
    expected_transfer: Decimal
    expected_credit: Decimal
    total: Decimal

class ObtenerSaldoCajaUseCase:
    """
    Application Use Case to query the current derived balance of a Cash Register session,
    providing breakdown by payment methods.
    """
    def __init__(self, repository: CajaRepository):
        self.repository = repository

    def execute(self, company_id: uuid.UUID, caja_id: uuid.UUID) -> SaldoCajaBreakdown:
        caja = self.repository.get_by_id(caja_id)
        if caja is None or caja.company_id != company_id:
            raise CajaNotFoundException(caja_id)

        expected_cash = Decimal("0.0000")
        expected_card = Decimal("0.0000")
        expected_transfer = Decimal("0.0000")
        expected_credit = Decimal("0.0000")

        for m in caja.movements:
            change = m.amount if m.type == "INGRESO" else -m.amount
            if m.payment_method == "EFECTIVO":
                expected_cash += change
            elif m.payment_method == "TARJETA":
                expected_card += change
            elif m.payment_method == "TRANSFERENCIA":
                expected_transfer += change
            elif m.payment_method == "CREDITO":
                expected_credit += change

        total = expected_cash + expected_card + expected_transfer + expected_credit

        return {
            "expected_cash": expected_cash,
            "expected_card": expected_card,
            "expected_transfer": expected_transfer,
            "expected_credit": expected_credit,
            "total": total
        }
