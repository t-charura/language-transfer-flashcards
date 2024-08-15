import typer
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from langchain_openai import ChatOpenAI
from openai import AuthenticationError, NotFoundError
from rich import print

from ltf import YoutubeTranscript
from ltf import utils
from ltf.config import settings
from ltf.models import FlashcardSet


class LanguageTransferFlashcards:
    """
    Create Flashcards from Language-Transfer YouTube videos using ChatGPT.

    This class provides functionality to download YouTube transcripts,
    process them with a language model, and generate flashcards.
    """

    def __init__(self, url: str, target_language: str):
        """
        Initialize the LanguageTransferFlashcards class

        Args:
            url: URL of the YouTube video
            target_language: The language that is taught in the YouTube video
        """
        self.title, self.transcript = YoutubeTranscript().download_from_url(url)
        self.target_language = target_language
        self.prompt_template = PromptTemplate(
            template=utils.load_template(),
            input_variables=["video_title", "target_language", "youtube_transcript"],
        )

    def _get_chain(self, llm: ChatOpenAI) -> RunnableSerializable:
        """
        Build the LLM chain to create flashcards.

        Args:
            llm: LLM model to use

        Returns:
            LLM chain
        """
        structured_output_llm = llm.with_structured_output(FlashcardSet)
        return self.prompt_template | structured_output_llm

    def _create_flashcards(self, llm: ChatOpenAI) -> FlashcardSet:
        """
        Create flashcards consisting of English and target language translations

        Args:
            llm: LLM model to use

        Returns:
            A set of flashcards

        Raises:
            AuthenticationError: If OpenAI API key is invalid
        """
        extraction_chain = self._get_chain(llm=llm)
        try:
            return extraction_chain.invoke(
                {
                    "video_title": self.title,
                    "target_language": self.target_language,
                    "youtube_transcript": self.transcript,
                }
            )
        except AuthenticationError:
            print(
                "Incorrect API key provided!\n"
                "You can find your API key at: https://platform.openai.com/account/api-keys.\n"
                "Please update the value in your .env file."
            )
            raise typer.Abort()
        except NotFoundError:
            print(
                f'The model "{llm.model_name}" does not exist or you do not have access to it.\n'
                f"You can find all available models at: https://platform.openai.com/docs/models\n"
                f"Please update the value in your .env file."
            )
            raise typer.Abort()

    def run(self, model_name: str, api_key: str, delimiter: str, exclude: str) -> None:
        """
        Create Flashcards from YouTube video and save them as CSV file

        Args:
            model_name: OpenAI model name to use
            api_key: OpenAI API key
            delimiter: Delimiter to use in CSV file
            exclude: Directory containing CSV files with words and sentences to exclude
        """
        llm = utils.initialize_llm(
            api_key=api_key if api_key else settings.OPENAI_API_KEY,
            model_name=model_name if model_name else settings.OPENAI_MODEL_NAME,
        )
        print(f"Using: [green bold]{llm.model_name}[/green bold]\n")

        flashcards = self._create_flashcards(llm=llm)
        utils.save_flashcards_as_csv(
            flashcards, filename=self.title, delimiter=delimiter, exclude=exclude
        )

    def save_prompt(self) -> None:
        """Create final prompt and save it as text file."""
        prompt_as_string = self.prompt_template.invoke(
            {
                "video_title": self.title,
                "target_language": self.target_language,
                "youtube_transcript": self.transcript,
            }
        ).text

        utils.save_prompt_as_txt(prompt_as_string, filename=self.title)
