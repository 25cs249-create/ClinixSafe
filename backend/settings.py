from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra = "ignore",
    )

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    engine_version: str = "1.0.0"
    kb_version: str = "1.0.0"

    log_level: str = "INFO"

    demo_mode: bool = True


    # --------------------------------------------------
    # Data
    # --------------------------------------------------

    kb_path: Path = Path("backend/data/knowledge_base.json")
    aliases_path: Path = Path("backend/data/medication_aliases.json")

    # --------------------------------------------------
    # Slashy (Partner Integration)
    # --------------------------------------------------

    slashy_enabled: bool = False

    slashy_api_key: str = ""

    slashy_base_url: str = ""

    slashy_timeout: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()