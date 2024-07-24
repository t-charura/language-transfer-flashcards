import re
import csv
import yaml
from pathlib import Path
from typing import Union, Any, Dict

from langchain_openai import ChatOpenAI

from ltf.config import settings
from ltf.language_transfer_flashcards import FlashcardSet

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_template():
    """Return prompt template as string"""
    with open(PROJECT_ROOT / 'ltf' / 'data' / 'prompt.yaml', 'r') as f:
        prompt = yaml.safe_load(f)
    return prompt.get('template')


def get_llm(api_key: str, mini: bool = False) -> ChatOpenAI:
    """Return LLM instance"""
    return ChatOpenAI(
        model_name=settings.GPT_4o_MINI if mini else settings.GPT_4o,
        api_key=api_key,
        temperature=0
    )


def clean_youtube_title(video_title: str) -> str:
    """
    Remove unwanted characters from the YouTube video title, because the title is used as a filename.

    Args:
        video_title: The title of the YouTube video

    Returns:
        The cleaned video title
    """
    allowed_chars = re.sub(r'[^a-z0-9 ]', '', video_title.lower())
    return (
        re.sub(r'\s+', ' ', allowed_chars)  # replace multiple spaces with a single space
        .replace(' ', '_')  # replace spaces with underscores
    )


def save_flashcards_as_csv_file(
        flashcard_set: Union[FlashcardSet, Dict[str, Any]],
        filename: str,
        delimiter: str = ';'
) -> None:
    """
    Create a CSV file with the flashcards in the FlashcardSet object.

    Args:
        flashcard_set: The FlashcardSet object containing the flashcards.
        filename: The name of the CSV file to be created.
        delimiter: The delimiter used in the CSV file. Defaults to ';'.
    """
    with open(f'{clean_youtube_title(filename)}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)

        for flashcard in flashcard_set.flashcards:
            writer.writerow([flashcard.english, flashcard.target_language])


def save_prompt_as_txt_file(
        prompt: str,
        filename: str
) -> None:
    """
    Save the prompt as a text file.

    Args:
        prompt: The prompt to be saved as a text file.
        filename: The name of the text file to be created.
    """
    with open(f'{clean_youtube_title(filename)}.txt', 'w', encoding='utf-8') as file:
        file.write(prompt)
