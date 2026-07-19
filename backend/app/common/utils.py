import uuid
from datetime import datetime, timezone

def generate_uuid4() -> str:
    """
    Generates a secure string UUID v4 representation.
    """
    return str(uuid.uuid4())

def get_utc_now() -> datetime:
    """
    Returns the current datetime in timezone-aware UTC representation.
    """
    return datetime.now(timezone.utc)
