from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from ltf.models import AvailableTargetLanguages, AvailableModels

CONFIG_DIR = Path.home() / ".ltf"


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: AvailableModels

    # Your target language from Language Transfer:
    TARGET_LANGUAGE: AvailableTargetLanguages

    model_config = SettingsConfigDict(env_file=(CONFIG_DIR / ".env"))


settings = Settings()
