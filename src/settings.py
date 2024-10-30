from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_dir: str = path.join(path.dirname(path.realpath(__file__)), "..")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=path.join(project_dir, "secrets/.env.prod"),
        extra="ignore",
        populate_by_name=True,
    )

    # Telegram
    bot_api_token: str

    # Google
    google_client_secrets: str

    # Cache
    redis_dsn: str
    fsm_state_ttl: int = 60 * 60 * 24 * 30  # 1 month
    fsm_data_ttl: int = 60 * 60 * 24 * 30  # 1 month

    # Storage
    db_dsn: str
