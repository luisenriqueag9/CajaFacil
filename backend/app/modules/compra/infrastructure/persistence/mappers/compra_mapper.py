from decimal import Decimal
from app.modules.compra.infrastructure.persistence.models.compra_model import Compra as DBOCompra, DetalleCompra as DBODetalleCompra
from app.modules.compra.domain.aggregates.compra import Compra
from app.modules.compra.domain.entities.detalle_compra import DetalleCompra
from app.modules.compra.domain.value_objects.cantidad import Cantidad
from app.modules.compra.domain.value_objects.dinero import Dinero
from app.modules.compra.domain.value_objects.estado_compra import EstadoCompra
from app.modules.compra.domain.value_objects.numero_compra import NumeroCompra

class CompraMapper:
    @staticmethod
    def to_db(domain: Compra) -> DBOCompra:
        """
        Convierte una entidad de dominio Compra en un modelo de base de datos SQLAlchemy.
        """
        db_details = [
            DBODetalleCompra(
                id=item.id,
                purchase_id=item.purchase_id,
                product_id=item.product_id,
                quantity=item.quantity.valor,
                unit_cost=item.unit_cost.monto
            )
            for item in domain.items
        ]
        db_purchase = DBOCompra(
            id=domain.id,
            company_id=domain.company_id,
            supplier_id=domain.supplier_id,
            invoice_number=domain.invoice_number.valor,
            payment_condition=domain.payment_condition,
            issue_date=domain.issue_date,
            status=domain.status.valor,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            details=db_details
        )
        return db_purchase

    @staticmethod
    def to_domain(db: DBOCompra) -> Compra:
        """
        Convierte un modelo de base de datos SQLAlchemy en una entidad de dominio Compra.
        """
        items = [
            DetalleCompra(
                id=item.id,
                purchase_id=item.purchase_id,
                product_id=item.product_id,
                quantity=Cantidad(item.quantity),
                unit_cost=Dinero(item.unit_cost)
            )
            for item in db.details
        ]
        
        return Compra(
            id=db.id,
            company_id=db.company_id,
            supplier_id=db.supplier_id,
            invoice_number=NumeroCompra(db.invoice_number),
            payment_condition=db.payment_condition,
            issue_date=db.issue_date,
            status=EstadoCompra(db.status),
            created_at=db.created_at,
            updated_at=db.updated_at,
            items=items
        )

    @staticmethod
    def update_db_model(db_model: DBOCompra, domain: Compra) -> None:
        """
        Copia campos editables de la entidad de dominio al modelo SQLAlchemy.
        """
        db_model.status = domain.status.valor
        db_model.updated_at = domain.updated_at
        
        # Durante borrador podemos actualizar lineas: limpiamos y recreamos
        db_model.details.clear()
        db_model.details.extend([
            DBODetalleCompra(
                id=item.id,
                purchase_id=item.purchase_id,
                product_id=item.product_id,
                quantity=item.quantity.valor,
                unit_cost=item.unit_cost.monto
            )
            for item in domain.items
        ])
PostInitMapping = True
