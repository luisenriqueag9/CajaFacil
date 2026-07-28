from app.modules.credito.infrastructure.persistence.models.credito_model import Credito as DBOCredito
from app.modules.credito.domain.aggregates.credito import Credito
from app.modules.credito.domain.value_objects.estado_credito import EstadoCredito
from app.modules.credito.domain.value_objects.dinero import Dinero

class CreditoMapper:
    @staticmethod
    def to_db(domain: Credito) -> DBOCredito:
        return DBOCredito(
            id=domain.id,
            company_id=domain.company_id,
            client_id=domain.client_id,
            credit_limit=domain.credit_limit.monto,
            balance=domain.balance.monto,
            status=domain.status.valor,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )

    @staticmethod
    def to_domain(db: DBOCredito) -> Credito:
        return Credito(
            id=db.id,
            company_id=db.company_id,
            client_id=db.client_id,
            credit_limit=Dinero(db.credit_limit),
            balance=Dinero(db.balance),
            status=EstadoCredito(db.status),
            created_at=db.created_at,
            updated_at=db.updated_at
        )

    @staticmethod
    def update_db_model(db_model: DBOCredito, domain: Credito) -> None:
        db_model.credit_limit = domain.credit_limit.monto
        db_model.balance = domain.balance.monto
        db_model.status = domain.status.valor
        db_model.updated_at = domain.updated_at
