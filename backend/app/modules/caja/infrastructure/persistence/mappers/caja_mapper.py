from app.modules.caja.infrastructure.persistence.models.caja_model import (
    Caja as DBOCaja,
    SesionCaja as DBOSesionCaja,
    MovimientoCaja as DBOMovimientoCaja,
    ArqueoCaja as DBOArqueoCaja
)
from app.modules.caja.domain.entities.caja import Caja
from app.modules.caja.domain.aggregates.sesion_caja import SesionCaja
from app.modules.caja.domain.entities.movimiento_caja import MovimientoCaja
from app.modules.caja.domain.entities.arqueo_caja import ArqueoCaja
from app.modules.caja.domain.value_objects.estado_sesion import EstadoSesion
from app.modules.caja.domain.value_objects.tipo_movimiento import TipoMovimiento
from app.modules.caja.domain.value_objects.metodo_pago import MetodoPago
from app.modules.caja.domain.value_objects.dinero import Dinero

class CajaMapper:
    # 1. Caja physical register mappings
    @staticmethod
    def caja_to_db(domain: Caja) -> DBOCaja:
        return DBOCaja(
            id=domain.id,
            company_id=domain.company_id,
            name=domain.name,
            status=domain.status,
            created_at=domain.created_at
        )

    @staticmethod
    def caja_to_domain(db: DBOCaja) -> Caja:
        return Caja(
            id=db.id,
            company_id=db.company_id,
            name=db.name,
            status=db.status,
            created_at=db.created_at
        )

    # 2. SesionCaja session mappings
    @staticmethod
    def sesion_to_db(domain: SesionCaja) -> DBOSesionCaja:
        db_session = DBOSesionCaja(
            id=domain.id,
            caja_id=domain.caja_id,
            company_id=domain.company_id,
            user_id=domain.user_id,
            status=domain.status.valor,
            opening_balance=domain.opening_balance.monto,
            opened_at=domain.opened_at,
            closed_at=domain.closed_at
        )

        db_session.movements = [
            DBOMovimientoCaja(
                id=m.id,
                sesion_id=domain.id,
                type=m.type.valor,
                amount=m.amount.monto,
                payment_method=m.payment_method.valor,
                concept=m.concept,
                origin_context=m.origin_context,
                origin_document_id=m.origin_document_id,
                voided=m.voided,
                created_at=m.created_at
            ) for m in domain.movements
        ]

        db_session.audits = [
            DBOArqueoCaja(
                id=a.id,
                sesion_id=domain.id,
                physical_amount=a.physical_amount.monto,
                system_amount=a.system_amount.monto,
                difference=a.difference.monto,
                supervisor_id=a.supervisor_id,
                created_at=a.created_at
            ) for a in domain.audits
        ]

        return db_session

    @staticmethod
    def sesion_to_domain(db: DBOSesionCaja) -> SesionCaja:
        movements = [
            MovimientoCaja(
                id=m.id,
                sesion_id=db.id,
                type=TipoMovimiento(m.type),
                amount=Dinero(m.amount),
                payment_method=MetodoPago(m.payment_method),
                concept=m.concept,
                origin_context=m.origin_context,
                origin_document_id=m.origin_document_id,
                voided=m.voided,
                created_at=m.created_at
            ) for m in db.movements
        ]

        audits = [
            ArqueoCaja(
                id=a.id,
                sesion_id=db.id,
                physical_amount=Dinero(a.physical_amount),
                system_amount=Dinero(a.system_amount),
                difference=Dinero(a.difference),
                supervisor_id=a.supervisor_id,
                created_at=a.created_at
            ) for a in db.audits
        ]

        return SesionCaja(
            id=db.id,
            caja_id=db.caja_id,
            company_id=db.company_id,
            user_id=db.user_id,
            status=EstadoSesion(db.status),
            opening_balance=Dinero(db.opening_balance),
            opened_at=db.opened_at,
            closed_at=db.closed_at,
            movements=movements,
            audits=audits
        )

    @staticmethod
    def update_sesion_db_model(db_model: DBOSesionCaja, domain: SesionCaja) -> None:
        db_model.status = domain.status.valor
        db_model.closed_at = domain.closed_at

        # Update movements
        db_mov_ids = {m.id for m in db_model.movements}
        for m in domain.movements:
            if m.id not in db_mov_ids:
                db_model.movements.append(
                    DBOMovimientoCaja(
                        id=m.id,
                        sesion_id=domain.id,
                        type=m.type.valor,
                        amount=m.amount.monto,
                        payment_method=m.payment_method.valor,
                        concept=m.concept,
                        origin_context=m.origin_context,
                        origin_document_id=m.origin_document_id,
                        voided=m.voided,
                        created_at=m.created_at
                    )
                )
            else:
                # Update voided status if it changed
                for db_m in db_model.movements:
                    if db_m.id == m.id:
                        db_m.voided = m.voided

        # Update audits
        db_aud_ids = {a.id for a in db_model.audits}
        for a in domain.audits:
            if a.id not in db_aud_ids:
                db_model.audits.append(
                    DBOArqueoCaja(
                        id=a.id,
                        sesion_id=domain.id,
                        physical_amount=a.physical_amount.monto,
                        system_amount=a.system_amount.monto,
                        difference=a.difference.monto,
                        supervisor_id=a.supervisor_id,
                        created_at=a.created_at
                    )
                )
