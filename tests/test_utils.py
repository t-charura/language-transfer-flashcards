import pytest

from ltf.utils import clean_youtube_title


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
def test_clean_youtube_title_basic_functionality(input_title, expected_output):
    assert clean_youtube_title(input_title) == expected_output


def test_clean_youtube_title_edge_cases():
    assert clean_youtube_title("!@#$%^&*()") == ""  # Only special characters
    assert clean_youtube_title("   ") == ""  # Only spaces
    assert clean_youtube_title("á é í ó ú") == ""  # Non-ASCII characters


def test_clean_youtube_title_error_handling():
    with pytest.raises(AttributeError):
        clean_youtube_title(None)

    with pytest.raises(AttributeError):
        clean_youtube_title(123)
