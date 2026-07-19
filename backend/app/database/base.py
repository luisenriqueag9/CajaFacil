from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 Unified Declarative Base.
    All database models across modules must inherit from this class to participate
    in migrations and session query capabilities.
    """
    # Force default __tablename__ if desired, or let concrete classes specify
    pass

# Note: For Alembic migrations autogenerate to work, all domain models
# from modules should be imported here so Alembic gathers their metadata.
#
# Example:
# from app.modules.product.data.models import ProductModel # noqa: F401
