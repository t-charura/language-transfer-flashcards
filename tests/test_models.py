import pytest

from ltf.models import (
    Flashcard,
    FlashcardSet,
    AvailableTargetLanguages,
)


def test_flashcard_creation():
    flashcard = Flashcard(english="Hello", target_language="Hola")
    assert flashcard.english == "Hello"
    assert flashcard.target_language == "Hola"


def test_flashcard_missing_field():
    with pytest.raises(ValueError):
        Flashcard(english="Hello")


def test_flashcard_set_creation():
    flashcards = [
        Flashcard(english="Hello", target_language="Hola"),
        Flashcard(english="Goodbye", target_language="Adiós"),
    ]
    flashcard_set = FlashcardSet(flashcards=flashcards)
    assert len(flashcard_set.flashcards) == 2
    assert flashcard_set.flashcards[0].english == "Hello"
    assert flashcard_set.flashcards[1].target_language == "Adiós"


def test_invalid_target_language():
    with pytest.raises(ValueError):
        AvailableTargetLanguages("InvalidLanguage")
