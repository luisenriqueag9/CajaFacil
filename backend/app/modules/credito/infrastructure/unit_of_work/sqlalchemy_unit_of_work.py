from app.database.unit_of_work import CommonSqlAlchemyUnitOfWork
from app.modules.credito.application.ports.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(CommonSqlAlchemyUnitOfWork, UnitOfWork):
    """
    Implementacion especifica del modulo Credito.
    Hereda el comportamiento transaccional del modulo comun.
    """
    pass
