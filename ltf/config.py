from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from ltf.models import AvailableTargetLanguages

ENV_DIR = Path.home() / ".ltf"


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: str = "gpt-4o"

    # The language you are currently learning form Language Transfer
    TARGET_LANGUAGE: Optional[AvailableTargetLanguages] = None

    # Testing
    FULL_CLI_TEST_WITH_EXTERNAL_DEPENDENCIES: bool = False

    # Load settings from .env file
    model_config = SettingsConfigDict(env_file=(ENV_DIR / ".env"))


settings = Settings()
