import pytest
from app.core.config import settings

def test_app_settings_initialization():
    """
    Validates that Pydantic settings are correctly loaded.
    """
    assert settings.APP_NAME is not None
    assert settings.ENV in ["development", "testing", "production"]
