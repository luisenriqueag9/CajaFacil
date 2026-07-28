from app.database.unit_of_work import CommonSqlAlchemyUnitOfWork
from app.modules.caja.application.ports.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(CommonSqlAlchemyUnitOfWork, UnitOfWork):
    """
    Implementacion transaccional especifica para el modulo Caja.
    Hereda la logica transaccional centralizada.
    """
    pass
