import csv
import re
from pathlib import Path
from typing import Union, Any, Dict

import yaml
from langchain_openai import ChatOpenAI
from rich import print

from ltf.config import settings
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
        model_name=model_name if model_name else settings.OPENAI_MODEL_NAME,
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
    flashcard_set: Union[FlashcardSet, Dict[str, Any]], filename: str, delimiter: str
) -> None:
    """
    Create a CSV file with the flashcards in the FlashcardSet object.

    Args:
        flashcard_set: The FlashcardSet object containing the flashcards.
        filename: The name of the CSV file to be created.
        delimiter: The delimiter used in the CSV file.
    """
    filename = f"{clean_youtube_title(filename)}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)

        for flashcard in flashcard_set.flashcards:
            writer.writerow([flashcard.english, flashcard.target_language])

    _show_file_location(filename)


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
