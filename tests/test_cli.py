import csv
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ltf.cli import app
from ltf.config import settings

runner = CliRunner()


def test_if_cli_csv_help_command_works():
    result = runner.invoke(app, ["csv", "--help"])
    assert result.exit_code == 0


@pytest.mark.skipif(
    not settings.FULL_CLI_TEST_WITH_EXTERNAL_DEPENDENCIES,
    reason="The Test requires access to the YouTube API.",
)
def test_incorrect_api_key():
    result = runner.invoke(
        app,
        [
            "csv",
            "https://www.youtube.com/watch?v=jIhkYHycv4M",
            "-l",
            "Swahili",
            "-m",
            "gpt-4o",
            "-k",
            "incorrect_api_key",
        ],
    )

    assert result.exit_code == 1
    assert "Incorrect API key provided!" in result.output


@pytest.mark.skipif(
    not settings.FULL_CLI_TEST_WITH_EXTERNAL_DEPENDENCIES,
    reason=(
        "The Test requires access to the YouTube and OpenAI API. "
        "Furthermore, it assumes that the .env file is located in: ~/.ltf/.env "
        "with a working OpenAI API key."
    ),
)
def test_csv_command():
    result = runner.invoke(
        app,
        [
            "csv",
            "https://www.youtube.com/watch?v=jIhkYHycv4M",
            "-l",
            "Swahili",
            "-m",
            "gpt-4o",
        ],
    )
    # Test if the command runs successfully
    assert result.exit_code == 0

    file_name = "complete_swahili_track_02_language_transfer_the_thinking_method.csv"

    def check_if_string_exists(target_string, csv_reader):
        return any(target_string in row[0] for row in csv_reader)

    with open(file_name) as flashcard_file:
        # Convert to list, since CSV file is less than 20 rows
        csv_reader_list = list(csv.reader(flashcard_file))

    # Test if the CSV file contains the correct data
    assert check_if_string_exists("sleep", csv_reader_list)
    assert check_if_string_exists("eat", csv_reader_list)
    assert check_if_string_exists("want", csv_reader_list)

    # Clean Up
    Path(file_name).unlink()


@pytest.mark.skipif(
    not settings.FULL_CLI_TEST_WITH_EXTERNAL_DEPENDENCIES,
    reason="The Test requires access to the YouTube API.",
)
def test_prompt_command():
    result = runner.invoke(
        app,
        [
            "prompt",
            "https://www.youtube.com/watch?v=jIhkYHycv4M",
            "-l",
            "Swahili",
        ],
    )
    # Test if the command runs successfully
    assert result.exit_code == 0

    file_name = "complete_swahili_track_02_language_transfer_the_thinking_method.txt"
    with open(file_name) as prompt_file:
        prompt_file_contents = prompt_file.read()

    # Test if the prompt contains the correct data
    assert (
        "Act as a language expert fluent in both Swahili and English."
        in prompt_file_contents
    )

    # Clean Up
    Path(file_name).unlink()
