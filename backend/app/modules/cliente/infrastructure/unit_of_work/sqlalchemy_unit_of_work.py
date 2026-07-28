from app.database.unit_of_work import CommonSqlAlchemyUnitOfWork
from app.modules.cliente.application.ports.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(CommonSqlAlchemyUnitOfWork, UnitOfWork):
    """
    Implementacion especifica del modulo Cliente.
    Hereda el comportamiento transaccional del modulo comun.
    """
    pass
