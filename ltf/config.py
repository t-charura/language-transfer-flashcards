from pathlib import Path
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # OPENAI settings
    OPENAI_API_KEY: str
    GPT_4o_MINI: str = 'gpt-4o-mini'

    # Your target language from Language Transfer:
    # TODO: link to availabe languages within your README
    TARGET_LANGUAGE: str = 'en'

    class Config:
        env_file = PROJECT_ROOT / '.env'


settings = Settings()
