import os
from typing import Literal
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "CajaFácil POS"
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    # Database configuration
    DB_PROVIDER: Literal["sqlite", "postgres"] = "sqlite"
    SQLITE_DB_PATH: str = "./caja_facil.db"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "secret_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "caja_facil_db"

    # Security placeholders
    SECRET_KEY: str = "super_secret_cryptographic_key_here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Dynamically constructs the database URL depending on the selected provider.
        """
        if self.DB_PROVIDER == "postgres":
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        # SQLite local database connection URL
        return f"sqlite:///{self.SQLITE_DB_PATH}"

# Singleton settings instance
settings = Settings()
