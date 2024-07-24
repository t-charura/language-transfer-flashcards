from typing import Literal
from pathlib import Path
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # OPENAI settings
    OPENAI_API_KEY: str
    GPT_4o_MINI: str = 'gpt-4o-mini'
    GPT_4o: str = 'gpt-4o'

    # Your target language from Language Transfer:
    TARGET_LANGUAGE: Literal[
        "Arabic", "French", "German", "Greek",
        "Italian", "Spanish", "Swahili", "Turkish"
    ]

    class Config:
        env_file = PROJECT_ROOT / '.env'


settings = Settings()
