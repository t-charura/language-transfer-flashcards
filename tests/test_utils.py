import csv

import pytest

from ltf import utils
from ltf.config import ENV_DIR
from ltf.models import Flashcard, FlashcardSet


@pytest.mark.parametrize(
    "input_title, expected_output",
    [
        ("Simple Title", "simple_title"),
        ("Title with UPPERCASE and 123", "title_with_uppercase_and_123"),
        ("  Title with spaces  ", "title_with_spaces"),
        ("Title with special chars !@#$%^&*()", "title_with_special_chars"),
        ("A" * 250, "a" * 200),  # Test truncation
        ("", ""),  # Test empty string
    ],
)
def test_clean_youtube_video_title_basic_functionality(input_title, expected_output):
    assert utils.clean_youtube_video_title(input_title) == expected_output


def test_clean_youtube_video_title_edge_cases():
    assert (
        utils.clean_youtube_video_title("!@#$%^&*()") == ""
    )  # Only special characters
    assert utils.clean_youtube_video_title("   ") == ""  # Only spaces
    assert utils.clean_youtube_video_title("á é í ó ú") == ""  # Non-ASCII characters


def test_env_information():
    assert str(ENV_DIR) in utils.env_information(ENV_DIR / ".env")


def test_read_env_file_file_not_found():
    # Test when the .env file does not exist
    with pytest.raises(FileNotFoundError):
        utils.read_env_file("non_existent_file.env")


def test_read_env_file_correct_file_reading(tmp_path, capfd):
    # Create a temporary .env file
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=ABCD1234\n"
        "OPENAI_MODEL_NAME=gpt-4o\n"
        "TARGET_LANGUAGE=Swahili\n"
    )

    # Call the function
    utils.read_env_file(env_file)

    # Capture and check output
    captured = capfd.readouterr()
    assert "OPENAI_API_KEY=ABCD1234" in captured.out
    assert "OPENAI_MODEL_NAME=gpt-4o" in captured.out
    assert "TARGET_LANGUAGE=Swahili" in captured.out


def test_save_flashcards_as_csv(tmp_path):
    # Create a temporary directory for our test file
    if not tmp_path.exists():
        tmp_path.mkdir()

    test_file = tmp_path / "test_flashcards.csv"

    # Create sample flashcards
    flashcards = [
        Flashcard(english="hello", target_language="bonjour"),
        Flashcard(english="goodbye", target_language="au revoir"),
        Flashcard(english="thank you", target_language="merci"),
    ]
    flashcard_set = FlashcardSet(flashcards=flashcards)

    # Call the function we're testing
    utils.save_flashcards_as_csv(
        flashcard_set, str(test_file), delimiter=",", exclude=""
    )

    # Check if the file was created
    assert test_file.exists()

    # Read the CSV file and check its contents
    with open(test_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Check if the number of rows matches the number of flashcards
    assert len(rows) == len(flashcards)

    # Check if each row contains the correct English and target language words
    for i, row in enumerate(rows):
        assert row[0] == flashcards[i].english
        assert row[1] == flashcards[i].target_language
