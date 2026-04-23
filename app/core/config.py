from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Seyalla Backend API")
    app_version: str = Field(default="0.2.0")
    environment: str = Field(default="dev")
    debug: bool = Field(default=False)

    # v1 uses in-memory seed data. Keep db url for migration readiness.
    database_url: str = Field(default="postgresql://postgres:postgres@localhost:5432/seyalla")

    model_config = SettingsConfigDict(env_prefix="SEYALLA_", env_file=".env", extra="ignore")


settings = Settings()
