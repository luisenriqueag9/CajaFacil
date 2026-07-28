from app.modules.caja.application.dto.sesion_caja_dto import SesionCajaDTO
from app.modules.caja.application.dto.movimiento_caja_dto import MovimientoCajaDTO
from app.modules.caja.application.dto.arqueo_caja_dto import ArqueoCajaDTO
from app.modules.caja.domain.aggregates.sesion_caja import SesionCaja

class SesionCajaDTOMapper:
    @staticmethod
    def to_dto(sesion: SesionCaja) -> SesionCajaDTO:
        mov_dtos = [
            MovimientoCajaDTO(
                id=m.id,
                sesion_id=m.sesion_id,
                type=m.type.valor,
                amount=m.amount.monto,
                payment_method=m.payment_method.valor,
                concept=m.concept,
                origin_context=m.origin_context,
                origin_document_id=m.origin_document_id,
                voided=m.voided,
                created_at=m.created_at
            ) for m in sesion.movements
        ]

        aud_dtos = [
            ArqueoCajaDTO(
                id=a.id,
                sesion_id=a.sesion_id,
                physical_amount=a.physical_amount.monto,
                system_amount=a.system_amount.monto,
                difference=a.difference.monto,
                supervisor_id=a.supervisor_id,
                created_at=a.created_at
            ) for a in sesion.audits
        ]

        return SesionCajaDTO(
            id=sesion.id,
            caja_id=sesion.caja_id,
            company_id=sesion.company_id,
            user_id=sesion.user_id,
            status=sesion.status.valor,
            opening_balance=sesion.opening_balance.monto,
            opened_at=sesion.opened_at,
            closed_at=sesion.closed_at,
            movements=mov_dtos,
            audits=aud_dtos
        )
