from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from ltf.models import AvailableTargetLanguages, AvailableModels

ENV_DIR = Path.home() / ".ltf"


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL_NAME: AvailableModels = AvailableModels.GPT_4o

    # The language you are currently learning form Language Transfer
    TARGET_LANGUAGE: Optional[AvailableTargetLanguages] = None

    model_config = SettingsConfigDict(env_file=(ENV_DIR / ".env"))


settings = Settings()
