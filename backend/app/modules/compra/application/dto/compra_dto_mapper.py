from app.modules.compra.application.dto.compra_dto import CompraDTO
from app.modules.compra.application.dto.detalle_compra_dto import DetalleCompraDTO
from app.modules.compra.domain.aggregates.compra import Compra
from app.modules.compra.domain.entities.detalle_compra import DetalleCompra

class CompraDTOMapper:
    @staticmethod
    def to_dto(compra: Compra) -> CompraDTO:
        items_dto = [
            DetalleCompraDTO(
                id=item.id,
                purchase_id=item.purchase_id,
                product_id=item.product_id,
                quantity=item.quantity.valor,
                unit_cost=item.unit_cost.monto,
                line_total=item.line_total.monto
            )
            for item in compra.items
        ]
        return CompraDTO(
            id=compra.id,
            company_id=compra.company_id,
            supplier_id=compra.supplier_id,
            invoice_number=str(compra.invoice_number),
            payment_condition=compra.payment_condition,
            issue_date=compra.issue_date,
            status=str(compra.status),
            created_at=compra.created_at,
            updated_at=compra.updated_at,
            items=items_dto,
            subtotal=compra.subtotal.monto,
            tax=compra.tax.monto,
            total=compra.total.monto
        )
