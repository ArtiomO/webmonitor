import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Service config."""

    name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASSWORD")
    host: str = os.environ.get("DB_HOST")
    port: str = os.environ.get("DB_PORT")
    log_level: str = os.environ.get("LOG_LEVEL")


cfg = Config()
