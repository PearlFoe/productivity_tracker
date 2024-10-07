from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    _project_dir: str = path.join(path.dirname(path.realpath(__file__)), "..")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=path.join(_project_dir, "secrets/.env"),
        extra="ignore",
        populate_by_name=True,
    )
    
    google_client_secrets: str
    calendar_id: str