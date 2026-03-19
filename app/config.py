from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bookmark Hub"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./bookmark_hub.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
