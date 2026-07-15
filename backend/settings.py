from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    engine_version: str = "1.0.0"
    kb_version: str = "1.0.0"

    log_level: str = "INFO"

    demo_mode: bool = True

    anthropic_api_key: str = ""

    model_name: str = "claude-3-5-sonnet-latest"

    temperature: float = 0.0

    kb_path: Path = Path("backend/data/knowledge_base.json")
    aliases_path: Path = Path("backend/data/medication_aliases.json")

@lru_cache
def get_settings():
    return Settings()