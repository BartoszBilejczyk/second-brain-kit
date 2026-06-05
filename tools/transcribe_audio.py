#!/usr/bin/env python3
"""
transcribe_audio.py — transcribe audio files using OpenAI Whisper.

Works with .m4a, .mp3, .wav, and most audio formats.

Usage:
  python tools/transcribe_audio.py <audio_file> [--model MODEL] [--output OUTPUT] [--language LANG]

Examples:
  python tools/transcribe_audio.py interview/recordings/session-01.m4a --output raw/transcripts/session-01.md
  python tools/transcribe_audio.py recording.m4a --model medium --language en
"""

import argparse
import sys
from datetime import date
from pathlib import Path

try:
    import whisper
except ImportError:
    print("Error: openai-whisper not installed.")
    print("Run: pip install -r tools/requirements.txt")
    sys.exit(1)


def transcribe_audio(
    audio_path: str,
    model_name: str = "small",
    output_path: str | None = None,
    language: str | None = None
) -> str:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path: Path to audio file (.m4a, .mp3, .wav, etc.)
        model_name: Whisper model — tiny (fast), small (balanced), medium (accurate)
        output_path: Path to save transcript; if None, prints to console
        language: Language code (e.g. 'en', 'pl'). Required — don't rely on auto-detect.

    Returns:
        Transcription text
    """
    print(f"Loading Whisper model: {model_name}…")
    model = whisper.load_model(model_name)

    print(f"Transcribing: {audio_path}")
    result = model.transcribe(
        audio_path,
        language=language,
        verbose=True
    )

    transcription = result["text"].strip()

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        frontmatter = (
            f"---\n"
            f"source: {Path(audio_path).name}\n"
            f"language: {language or 'unknown'}\n"
            f"date: {date.today().isoformat()}\n"
            f"model: {model_name}\n"
            f"---\n\n"
        )
        output_file.write_text(frontmatter + transcription, encoding="utf-8")
        print(f"\nTranscript saved to: {output_path}")

    return transcription


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using OpenAI Whisper"
    )
    parser.add_argument(
        "audio_file",
        help="Path to audio file (.m4a, .mp3, .wav, etc.)"
    )
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "small", "medium", "large"],
        help="Whisper model size (default: small). tiny=fast, small=balanced, medium=accurate"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path for transcript. Defaults to: raw/transcripts/<audio_stem>.md"
    )
    parser.add_argument(
        "--language", "-l",
        required=True,
        help="Language code — e.g. 'en' for English, 'pl' for Polish. Required."
    )

    args = parser.parse_args()

    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {args.audio_file}")
        sys.exit(1)

    # Default output: raw/transcripts/<stem>.md relative to repo root
    if args.output:
        output_path = args.output
    else:
        repo_root = Path(__file__).parent.parent
        output_path = str(repo_root / "raw" / "transcripts" / f"{audio_path.stem}.md")
        print(f"No --output specified. Will save to: {output_path}")

    try:
        transcribe_audio(
            str(audio_path),
            model_name=args.model,
            output_path=output_path,
            language=args.language
        )
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
