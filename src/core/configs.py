import os
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = pathlib.Path(__file__).parents[1]


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    DB_USER: str = os.environ.get("DB_USER", "")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
    DB_PORT: str = os.environ.get("DB_PORT", "")
    DB_HOST: str = os.environ.get("DB_HOST", "")
    DB_NAME: str = os.environ.get("DB_NAME", "")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")


class Settings(BaseSettings):

    db_settings: DBSettings = DBSettings()
    app_settings: AppSettings = AppSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
