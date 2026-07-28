from app.modules.cliente.infrastructure.persistence.models.cliente_model import Cliente as DBOCliente
from app.modules.cliente.domain.aggregates.cliente import Cliente
from app.modules.cliente.domain.value_objects.nombre_cliente import NombreCliente
from app.modules.cliente.domain.value_objects.estado_cliente import EstadoCliente
from app.modules.cliente.domain.value_objects.email_cliente import EmailCliente

class ClienteMapper:
    @staticmethod
    def to_db(domain: Cliente) -> DBOCliente:
        return DBOCliente(
            id=domain.id,
            company_id=domain.company_id,
            name=domain.name.valor,
            tax_id=domain.tax_id,
            phone=domain.phone,
            email=domain.email.valor if domain.email.valor else None,
            status=domain.status.valor,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )

    @staticmethod
    def to_domain(db: DBOCliente) -> Cliente:
        return Cliente(
            id=db.id,
            company_id=db.company_id,
            name=NombreCliente(db.name),
            tax_id=db.tax_id,
            phone=db.phone,
            email=EmailCliente(db.email),
            status=EstadoCliente(db.status),
            created_at=db.created_at,
            updated_at=db.updated_at
        )

    @staticmethod
    def update_db_model(db_model: DBOCliente, domain: Cliente) -> None:
        db_model.name = domain.name.valor
        db_model.tax_id = domain.tax_id
        db_model.phone = domain.phone
        db_model.email = domain.email.valor if domain.email.valor else None
        db_model.status = domain.status.valor
        db_model.updated_at = domain.updated_at
