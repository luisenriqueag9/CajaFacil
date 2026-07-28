from app.database.unit_of_work import CommonSqlAlchemyUnitOfWork
from app.modules.compra.application.ports.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(CommonSqlAlchemyUnitOfWork, UnitOfWork):
    """
    Implementacion especifica del modulo Compra.
    Hereda el comportamiento transaccional del modulo comun.
    """
    pass
