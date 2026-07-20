from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logger import logger

# Connection tuning parameters
connect_args = {}

if settings.DB_PROVIDER == "sqlite":
    # SQLite connection requires check_same_thread=False for multithreaded FastAPI requests
    connect_args["check_same_thread"] = False
    logger.info("Initializing SQLite database engine.")
else:
    logger.info("Initializing PostgreSQL database engine.")

# Create the Engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verification of connection validity before queries
    echo=False          # Turn on SQL logs by setting to True during debugging
)

# Enforce foreign key constraints in SQLite
if settings.DB_PROVIDER == "sqlite":
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if not hasattr(dbapi_connection, "cursor"):
            logger.error(f"dbapi_connection type: {type(dbapi_connection)}, dir: {dir(dbapi_connection)}")
            return
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Sessionmaker configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a transactional database session.
    Automatically closes the session after the request finishes or handles rollbacks.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
