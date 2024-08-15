import typer
from rich import print

from ltf import LanguageTransferFlashcards
from ltf import utils
from ltf.cli import validate
from ltf.config import ENV_DIR
from ltf.models import AvailableTargetLanguages

app = typer.Typer(name="Language Transfer Flashcards")


@app.command(
    name="csv",
    help="Create flashcards from Language-Transfer YouTube videos in CSV format",
)
def create_flashcards(
    url: str = typer.Argument(
        help='YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"'
    ),
    target_language: AvailableTargetLanguages = typer.Option(
        None,
        "--target-language",
        "-l",
        callback=validate.target_language,
        help="Target language taught in video. If None, takes value from .env file, located in: ~/.ltf/.env",
    ),
    model_name: str = typer.Option(
        None,
        "--model",
        "-m",
        help="OpenAI model name. If None, takes value from .env file. Defaults to gpt-4o if .env file does not exist",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        callback=validate.api_key,
        help="OpenAI API key. If None, takes value from .env file, located in: ~/.ltf/.env",
    ),
    delimiter: str = typer.Option(
        ",", "--delimiter", "-d", help="Delimiter to use in CSV file"
    ),
    exclude: str = typer.Option(
        None,
        "--exclude",
        "-e",
        help="Directory containing CSV files with words and sentences to exclude",
    ),
):
    flashcard_extraction = LanguageTransferFlashcards(
        url, target_language=target_language
    )
    flashcard_extraction.run(
        model_name=model_name, api_key=api_key, delimiter=delimiter, exclude=exclude
    )


@app.command(
    name="prompt",
    help="Create and save prompt with YouTube transcript to use it with your favorite LLM",
)
def create_prompt(
    url: str = typer.Argument(
        help='YouTube video url, e.g. "https://www.youtube.com/watch?v=VIDEO_ID"'
    ),
    target_language: AvailableTargetLanguages = typer.Option(
        None,
        "--target-language",
        "-l",
        callback=validate.target_language,
        help="Target language taught in video. If None, takes value from .env file",
    ),
):
    flashcard_extraction = LanguageTransferFlashcards(
        url, target_language=target_language
    )
    flashcard_extraction.save_prompt()


@app.command(name="env-location", help="Show location of your .env file")
def env_location():
    print(utils.env_information(ENV_DIR / ".env"))


@app.command(name="env-values", help="Show current values of your .env file")
def env_values():
    utils.read_env_file(ENV_DIR / ".env")
