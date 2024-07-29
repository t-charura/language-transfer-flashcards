import typer
from rich import print

from ltf import LanguageTransferFlashcards
from ltf.config import CONFIG_DIR
from ltf.models import AvailableTargetLanguages, AvailableModels

app = typer.Typer(name='Language Transfer Flashcards')


@app.command(name='csv', help='Create flashcards from Language-Transfer YouTube videos in CSV format')
def create_flashcards(
    url: str = typer.Argument(help='YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"'),
    target_language: AvailableTargetLanguages = typer.Option(
        None, '--target-language', '-l',
        help='Target language taught in video. If None, takes value from .env file, located in: ~/.ltf/.env'
    ),
    model_name: AvailableModels = typer.Option(
        None, '--model', '-m',
        help='OpenAI model name to use. If None, takes value from .env file, located in: ~/.ltf/.env'
    ),
    api_key: str = typer.Option(
        None, '--api-key', '-k',
        help='OpenAI API key. If None, takes value from .env file, located in: ~/.ltf/.env'
    ),
    delimiter: str = typer.Option(',', '--delimiter', '-d', help='Delimiter to use in CSV file')
):
    flashcard_extraction = LanguageTransferFlashcards(url, target_language=target_language)
    flashcard_extraction.run(model_name=model_name, api_key=api_key, delimiter=delimiter)


@app.command(name='prompt', help='Create and save prompt with YouTube transcript to use it with your favorite LLM')
def create_prompt(
    url: str = typer.Argument(help='YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"'),
    target_language: AvailableTargetLanguages = typer.Option(
        None, '--target-language', '-l',
        help='Target language taught in video. If None, takes value from .env file'
    )
):
    flashcard_extraction = LanguageTransferFlashcards(url, target_language=target_language)
    flashcard_extraction.save_prompt()


@app.command(name='env-location', help='Show location of your .env file')
def env_location():
    print(
        'Language-Transfer Flashcards (ltf) is looking for the .env file at the following location:\n'
        f'--> [green bold]{CONFIG_DIR / ".env"}[/green bold] <--\n\n'
        
        'If the file does not exist, please create it and set the following variables:\n'
        '"OPENAI_API_KEY", "OPENAI_MODEL_NAME" and "TARGET_LANGUAGE". \n\n'
        'Check https://github.com/t-charura/language-transfer-flashcards for an example .env file.'
    )
