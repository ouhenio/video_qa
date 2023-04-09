import os

import whisper
from rich.console import Console

console = Console()


class LocalWhisperTranscriber:
    def __init__(self, model_version):
        self.model = whisper.load_model(model_version)

    def transcribe(self, audio_path):
        console.print("🗣️  Initializing Local Whisper transcriber...", style="bold")

        # Check if the transcript already exists
        transcript_path = f"{audio_path.split('.')[0]}.txt"
        if not os.path.exists(transcript_path):
            console.print(f"\t↪ Transcribing {audio_path}...", style="bold")

            # Convert the MP3 file to text using the local Whisper model
            full_transcript = self.model.transcribe(audio_path)["text"]

            # Save the transcript to a text file
            with open(transcript_path, "w") as f:
                f.write(full_transcript)
                console.print(
                    f"""
                \t\t↪ saved transcript to {audio_path.split('.')[0]}.txt
                \t↪ word count: {len(full_transcript.split())}""",
                    style="bold",
                )

        else:
            # Load the transcript from the text file
            with open(transcript_path, "r") as f:
                full_transcript = f.read()

        console.print(
            f"""↪ Total words: {len(full_transcript.split())}
            ↪ Total characters: {len(full_transcript)}""",
            style="bold",
        )

        return full_transcript, transcript_path
