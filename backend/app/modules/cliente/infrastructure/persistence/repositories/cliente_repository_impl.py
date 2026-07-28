from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.database.repositories.base import BaseRepository
from app.modules.cliente.domain.aggregates.cliente import Cliente
from app.modules.cliente.domain.repositories.cliente_repository import ClienteRepository
from app.modules.cliente.infrastructure.persistence.models.cliente_model import Cliente as DBOCliente
from app.modules.cliente.infrastructure.persistence.mappers.cliente_mapper import ClienteMapper
from app.modules.cliente.domain.exceptions.cliente_no_encontrado_exception import ClienteNoEncontradoException

class ClienteRepositoryImpl(BaseRepository[DBOCliente], ClienteRepository):
    """
    Implementacion concreta de la interfaz ClienteRepository utilizando SQLAlchemy.
    """
    def __init__(self, db: Session):
        super().__init__(DBOCliente, db)

    def create(self, cliente: Cliente) -> Cliente:
        db_client = ClienteMapper.to_db(cliente)
        self.db.add(db_client)
        self.db.flush()
        return ClienteMapper.to_domain(db_client)

    def get_by_id(self, client_id: UUID) -> Cliente | None:
        statement = select(DBOCliente).where(DBOCliente.id == client_id)
        db_client = self.db.execute(statement).scalar_one_or_none()
        return ClienteMapper.to_domain(db_client) if db_client else None

    def get_by_tax_id(self, company_id: UUID, tax_id: str) -> Cliente | None:
        statement = select(DBOCliente).where(
            and_(
                DBOCliente.company_id == company_id,
                DBOCliente.tax_id == tax_id
            )
        )
        db_client = self.db.execute(statement).scalar_one_or_none()
        return ClienteMapper.to_domain(db_client) if db_client else None

    def get_all(self, company_id: UUID, status: str | None = None) -> list[Cliente]:
        statement = select(DBOCliente).where(DBOCliente.company_id == company_id)
        if status:
            statement = statement.where(DBOCliente.status == status)
            
        statement = statement.order_by(DBOCliente.name.asc())
        db_clients = self.db.execute(statement).scalars().all()
        return [ClienteMapper.to_domain(c) for c in db_clients]

    def update(self, cliente: Cliente) -> Cliente:
        statement = select(DBOCliente).where(DBOCliente.id == cliente.id)
        db_client = self.db.execute(statement).scalar_one_or_none()
        if not db_client:
            raise ClienteNoEncontradoException(cliente.id)

        ClienteMapper.update_db_model(db_client, cliente)
        self.db.flush()
        self.db.refresh(db_client)
        return ClienteMapper.to_domain(db_client)
