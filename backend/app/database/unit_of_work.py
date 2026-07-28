from sqlalchemy.orm import Session

class CommonSqlAlchemyUnitOfWork:
    """
    Implementacion base reutilizable de Unit of Work para SQLAlchemy.
    Encapsula el manejo transaccional de la sesion (context manager y commits).
    """
    def __init__(self, session: Session):
        self.session = session
        self._transaction = None

    def __enter__(self) -> "CommonSqlAlchemyUnitOfWork":
        # Encapsula transacciones anidadas (savepoints)
        self._transaction = self.session.begin_nested()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        if self._transaction:
            try:
                self._transaction.commit()
            except Exception:
                self._transaction = None
                raise
            self._transaction = None
        self.session.commit()

    def rollback(self) -> None:
        if self._transaction:
            try:
                self._transaction.rollback()
            except Exception:
                self._transaction = None
                raise
            self._transaction = None
        self.session.rollback()
