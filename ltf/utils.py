import csv
import re
from pathlib import Path
from typing import Union, Any, Dict

import yaml
from langchain_openai import ChatOpenAI
from rich import print

from ltf.models import FlashcardSet

PROJECT_DIR = Path(__file__).resolve().parent.parent


def load_template() -> str:
    """Return prompt template as string"""
    with open(PROJECT_DIR / "ltf" / "data" / "prompt.yaml", "r") as f:
        prompt = yaml.safe_load(f)
    return prompt.get("template")


def initialize_llm(api_key: str, model_name: str) -> ChatOpenAI:
    """
    Return an LLM instance

    Args:
        api_key: OpenAI API key
        model_name: OpenAI model name to use

    Returns:
        LLM instance
    """
    return ChatOpenAI(
        model_name=model_name,
        api_key=api_key,
        temperature=0,
    )


def clean_youtube_title(video_title: str) -> str:
    """
    Remove unwanted characters from the YouTube video title, because the title is used as a filename.

    Args:
        video_title: The title of the YouTube video

    Returns:
        The cleaned video title
    """
    allowed_chars = re.sub(r"[^a-z0-9 ]", "", video_title.lower()).strip()
    return re.sub(r"\s+", " ", allowed_chars).replace(" ", "_")[0:200]


def save_flashcards_as_csv(
    flashcard_set: Union[FlashcardSet, Dict[str, Any]],
    filename: str,
    delimiter: str,
    exclude: str,
) -> None:
    """
    Create a CSV file with the flashcards in the FlashcardSet object.

    Args:
        flashcard_set: The FlashcardSet object containing the flashcards.
        filename: The name of the CSV file to be created.
        delimiter: The delimiter used in the CSV file.
        exclude: The directory containing CSV files with words and sentences to exclude.
    """
    existing_flashcards = _load_existing_flashcards(exclude) if exclude else set()

    filename = f"{clean_youtube_title(filename)}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)

        writer.writerows(
            [
                [flashcard.english, flashcard.target_language]
                for flashcard in flashcard_set.flashcards
                if not exclude
                or flashcard.english.strip().lower() not in existing_flashcards
            ]
        )

    _show_file_location(filename)


def _load_existing_flashcards(directory: str) -> set:
    """
    Load existing flashcards from CSV files in the specified directory. Only get the English words.

    Args:
        directory: The directory containing the CSV files.

    Returns:
        A set of English words.
    """
    keys = set()
    directory_path = Path(directory)
    if not directory_path.exists():
        print(
            f'Directory: "{directory}" does not exist. '
            f"Continuing without loading existing flashcards.\n"
        )
        return keys

    return {
        row[0].strip().lower()
        for csv_file in directory_path.glob("*.csv")
        for row in csv.reader(csv_file.open("r"))
    }


def save_prompt_as_txt(prompt: str, filename: str) -> None:
    """
    Save the prompt as a text file.

    Args:
        prompt: The prompt to be saved as a text file.
        filename: The name of the text file to be created.
    """
    filename = f"{clean_youtube_title(filename)}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(prompt)

    _show_file_location(filename)


def _show_file_location(filename: str) -> None:
    """
    Print the location of the created file.

    Args:
        filename: The name of the file to be printed.
    """
    cwd = Path.cwd()
    print(f'File saved at: "{cwd / filename}"')


def env_information(file_path: Path) -> str:
    return (
        "Language Transfer Flashcards (ltf) is looking for the .env file at the following location:\n"
        f"--> [green bold]{file_path}[/green bold] <--\n\n"
        "File must contain the following variables: 'OPENAI_API_KEY', 'OPENAI_MODEL_NAME' and 'TARGET_LANGUAGE'. \n"
        "To see all valid values for these variables, run 'ltf csv --help'\n\n"
        "Check https://github.com/t-charura/language-transfer-flashcards for an example .env file."
    )


def read_env_file(file_path: Union[Path, str]) -> None:
    """
    Read the .env file and print the content to the console.

    Args:
        file_path: The path to the .env file.

    Raises:
        FileNotFoundError: If the .env file does not exist.
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(
            f".env file does not exist at: '{file_path}'. \n\n"
            f"Please create the file. For more information run 'ltf env-location'."
        )

    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            # Strip leading/trailing whitespace and skip comments and empty lines
            line = line.strip()
            if line and not line.startswith("#"):
                print(line)
