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
from app.modules.product.data.models import Product  # noqa: F401
from app.modules.unit.data.models import Unit  # noqa: F401
from app.modules.category.data.models import Category  # noqa: F401
from app.modules.company.data.models import Company  # noqa: F401

