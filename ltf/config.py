from pathlib import Path

from pydantic_settings import BaseSettings

from ltf.models import AvailableTargetLanguages

CONFIG_DIR = Path.home() / '.ltf'


class Settings(BaseSettings):
    # OPENAI settings
    OPENAI_API_KEY: str
    GPT_4o_MINI: str = 'gpt-4o-mini'
    GPT_4o: str = 'gpt-4o'

    # Your target language from Language Transfer:
    TARGET_LANGUAGE: AvailableTargetLanguages

    class Config:
        env_file = CONFIG_DIR / '.env'


settings = Settings()
