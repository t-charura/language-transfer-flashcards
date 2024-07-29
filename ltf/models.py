from enum import Enum
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class Flashcard(BaseModel):
    """Represents a single vocabulary flashcard with translations between English and a target language."""
    english: str = Field(
        ...,  # This makes the field required
        description="The English word, phrase, or sentence to be learned.",
    )
    target_language: str = Field(
        ...,
        description="The translation of the English text in the {target_language}.",
    )


class FlashcardSet(BaseModel):
    """Represents a collection of vocabulary flashcards for a specific language pair."""
    flashcards: List[Flashcard] = Field(
        ...,
        description="A list of Flashcard objects containing vocabulary pairs."
    )


class AvailableTargetLanguages(str, Enum):
    """Enum containing all available target languages."""
    ARABIC = "Arabic"
    FRENCH = "French"
    GERMAN = "German"
    GREEK = "Greek"
    ITALIAN = "Italian"
    SPANISH = "Spanish"
    SWAHILI = "Swahili"
    TURKISH = "Turkish"


class AvailableModels(str, Enum):
    """Enum containing all available models."""
    # o-Models
    GPT_4o = 'gpt-4o'
    GPT_4o_MINI = 'gpt-4o-mini'

    # Regular Models
    GPT_4_TURBO = 'gpt-4-turbo'
    GPT_3_5_TURBO = 'gpt-3.5-turbo'  # not recommended - use 4o mini
