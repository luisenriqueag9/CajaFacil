from uuid import UUID
from app.modules.venta.domain.events.venta_events import VentaConfirmada, VentaAnulada
from app.modules.venta.application.ports.movimiento_inventario_repository import MovimientoInventarioRepository
from app.modules.venta.application.ports.movimiento_caja_repository import MovimientoCajaRepository
from app.modules.venta.application.ports.credito_repository import CreditoRepository

class VentaEventHandler:
    """
    Application handlers for Venta events.
    Applies consistency changes sychronously across domains (Inventory, Cash Box, Credit)
    using the shared database transaction.
    """
    def __init__(
        self,
        inventario_repo: MovimientoInventarioRepository,
        caja_repo: MovimientoCajaRepository,
        credito_repo: CreditoRepository
    ):
        self.inventario_repo = inventario_repo
        self.caja_repo = caja_repo
        self.credito_repo = credito_repo

    def handle_confirmada(self, event: VentaConfirmada) -> None:
        """
        Subscribes to VentaConfirmada to register inventory, box, and credit changes.
        """
        # 1. Register inventory output (SALIDA) for each product sold
        for item in event.items:
            self.inventario_repo.registrar_movimiento(
                company_id=event.company_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                tipo="SALIDA",
                concept="VENTA",
                reference_id=event.venta_id
            )

        # 2. Register cash entry (INGRESO) if cash was accepted
        if event.cash_amount > 0:
            self.caja_repo.registrar_movimiento(
                company_id=event.company_id,
                box_id=event.box_id,
                user_id=event.user_id,
                amount=event.cash_amount,
                tipo="INGRESO",
                concept="VENTA",
                reference_id=event.venta_id
            )

        # 3. Register client debt if credit was approved
        if event.credit_amount > 0 and event.client_id:
            self.credito_repo.registrar_deuda(
                company_id=event.company_id,
                client_id=event.client_id,
                amount=event.credit_amount,
                reference_id=event.venta_id
            )

    def handle_anulada(self, event: VentaAnulada) -> None:
        """
        Subscribes to VentaAnulada to reverse inventory, box, and credit changes.
        """
        # 1. Register inventory input (ENTRADA) for each product returned
        for item in event.items:
            self.inventario_repo.registrar_movimiento(
                company_id=event.company_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                tipo="ENTRADA",
                concept="ANULACION_VENTA",
                reference_id=event.venta_id
            )

        # 2. Register cash exit (EGRESO) to refund cash
        if event.cash_amount > 0:
            self.caja_repo.registrar_movimiento(
                company_id=event.company_id,
                box_id=event.box_id,
                user_id=event.voided_by,
                amount=event.cash_amount,
                tipo="EGRESO",
                concept="ANULACION_VENTA",
                reference_id=event.venta_id
            )

        # 3. Reverse client debt
        if event.credit_amount > 0 and event.client_id:
            self.credito_repo.reversar_deuda(
                company_id=event.company_id,
                client_id=event.client_id,
                amount=event.credit_amount,
                reference_id=event.venta_id
            )
