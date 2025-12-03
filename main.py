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
import json
import time
from pathlib import Path
from typing import Any

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


def transcribe_audio(
    client: AzureOpenAI,
    audio_file_path: str,
    model: str,
    response_format: str = "verbose_json",
) -> Any:
    """Run a transcription request for the specified model."""
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format=response_format,
        )
    return result


def format_response_json(response: Any) -> str:
    """Return a pretty JSON string of the transcription response for debugging."""
    if hasattr(response, "model_dump_json"):
        raw_json = response.model_dump_json()
        try:
            parsed = json.loads(raw_json)
        except json.JSONDecodeError:
            return raw_json
        return json.dumps(parsed, ensure_ascii=False, indent=2)

    if hasattr(response, "model_dump"):
        payload = response.model_dump()
    elif hasattr(response, "to_dict"):
        payload = response.to_dict()
    else:
        payload = getattr(response, "__dict__", response)

    return json.dumps(payload, ensure_ascii=False, indent=2, default=str)


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
        {"name": "whisper", "response_format": "json"},
        {"name": "gpt-4o-transcribe", "response_format": "json"},
        {"name": "gpt-4o-mini-transcribe", "response_format": "json"},
        {"name": "gpt-4o-transcribe-diarize", "response_format": "diarized_json"},
    ]

    # Run transcription with each model
    for model in models:
        model_name = model["name"]
        response_format = model["response_format"]
        print(f"\n【{model_name}】")
        print("-" * 40)
        start_time = time.perf_counter()
        try:
            response = transcribe_audio(
                client,
                audio_file_path,
                model_name,
                response_format=response_format,
            )
            print(response.text)
            print("\n[Debug] Response JSON:")
            print(format_response_json(response))
            elapsed = time.perf_counter() - start_time
            print(f"\nExecution time: {elapsed:.3f} seconds")
        except Exception as e:
            print(f"Error: {e}")
            elapsed = time.perf_counter() - start_time
            print(f"Execution time before error: {elapsed:.3f} seconds")
        print()


if __name__ == "__main__":
    main()
