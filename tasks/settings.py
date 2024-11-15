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

    # Google
    google_client_secrets: str

    # Storage
    db_dsn: str
