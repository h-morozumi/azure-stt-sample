"""
Azure OpenAI Speech-to-Text Sample Application

This application compares 4 Azure OpenAI transcription models:
- Whisper
- gpt-4o-transcribe
- gpt-4o-mini-transcribe
- gpt-4o-transcribe-diarize

Usage:
    uv run main.py ./audio/your-audio-file.mp3
"""

import sys
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()


def get_client() -> AzureOpenAI:
    """Create and return an Azure OpenAI client."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set in .env file"
        )

    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )


def transcribe_with_whisper(client: AzureOpenAI, audio_file_path: str) -> str:
    """
    Transcribe audio using the Whisper model.

    Args:
        client: Azure OpenAI client
        audio_file_path: Path to the audio file

    Returns:
        Transcribed text
    """
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="whisper",
            file=audio_file,
        )
    return result.text


def transcribe_with_gpt4o_transcribe(client: AzureOpenAI, audio_file_path: str) -> str:
    """
    Transcribe audio using the gpt-4o-transcribe model.

    Args:
        client: Azure OpenAI client
        audio_file_path: Path to the audio file

    Returns:
        Transcribed text
    """
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file,
        )
    return result.text


def transcribe_with_gpt4o_mini_transcribe(
    client: AzureOpenAI, audio_file_path: str
) -> str:
    """
    Transcribe audio using the gpt-4o-mini-transcribe model.

    Args:
        client: Azure OpenAI client
        audio_file_path: Path to the audio file

    Returns:
        Transcribed text
    """
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
        )
    return result.text


def transcribe_with_gpt4o_transcribe_diarize(
    client: AzureOpenAI, audio_file_path: str
) -> str:
    """
    Transcribe audio using the gpt-4o-transcribe model with diarization.

    Args:
        client: Azure OpenAI client
        audio_file_path: Path to the audio file

    Returns:
        Transcribed text with speaker identification
    """
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
        )
    return result.text


def main():
    """Main function to run the transcription comparison."""
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <audio_file_path>")
        print("Example: uv run main.py ./audio/sample.mp3")
        sys.exit(1)

    audio_file_path = sys.argv[1]

    # Check if the audio file exists
    if not Path(audio_file_path).exists():
        print(f"Error: Audio file not found: {audio_file_path}")
        sys.exit(1)

    print(f"Transcribing audio file: {audio_file_path}")
    print("=" * 60)

    try:
        client = get_client()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Define the models and their corresponding functions
    models = [
        ("Whisper", transcribe_with_whisper),
        ("gpt-4o-transcribe", transcribe_with_gpt4o_transcribe),
        ("gpt-4o-mini-transcribe", transcribe_with_gpt4o_mini_transcribe),
        ("gpt-4o-transcribe-diarize", transcribe_with_gpt4o_transcribe_diarize),
    ]

    # Run transcription with each model
    for model_name, transcribe_func in models:
        print(f"\n【{model_name}】")
        print("-" * 40)
        try:
            result = transcribe_func(client, audio_file_path)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
        print()


if __name__ == "__main__":
    main()
