import os

import openai
from dotenv import load_dotenv
from pydub import AudioSegment
from rich import print
from rich.console import Console

console = Console()


class WhisperTranscriber:
    def __init__(self, api_key):
        load_dotenv()
        openai.api_key = api_key
        self.openai_price = float(os.getenv("OPENAI_PRICING_WHISPER"))

    def chunk(self, audio_path):
        file_name = os.path.basename(audio_path)
        file_size = os.path.getsize(audio_path)
        audio_list = []

        # Get length of audio file
        audio = AudioSegment.from_mp3(audio_path)
        duration = audio.duration_seconds
        est_cost = duration * self.openai_price / 60
        console.print(f"↪ 💵 Estimated cost: ${est_cost:.2f} ({(duration / 60):.2f} minutes)", style="bold")

        if file_size > 25 * 1024 * 1024:
            console.print(
                f"""
            ↪ The audio file is too large:
            {(file_size / 1024 / 1024):.2f} MB (>25MB), chunking...""",
                style="bold",
            )

            # check if chunks already exist
            if os.path.exists(f"downloads/whisper/{file_name.split('.')[0]}_0.mp3"):
                console.print("↪ Chunks already exist, loading...", style="bold")
                for i in range(100):
                    chunk_name = f"downloads/whisper/{file_name.split('.')[0]}_{i}.mp3"
                    if os.path.exists(chunk_name):
                        audio_list.append(chunk_name)
                    else:
                        return audio_list

            audio = AudioSegment.from_mp3(audio_path)

            # PyDub handles time in milliseconds
            chunk = 25 * 60 * 1000

            # split the audio file into ~25 minute chunks
            for i, chunk in enumerate(audio[::chunk]):
                chunk_name = f"downloads/whisper/{file_name.split('.')[0]}_{i}.mp3"

                if os.path.exists(chunk_name):
                    pass

                audio_list.append(chunk_name)
                chunk.export(chunk_name, format="mp3")

        else:
            audio_list.append(audio_path)

        return audio_list

    def transcribe(self, audio_path):
        console.print("🗣️  Initializing Whisper transcriber...", style="bold")

        audio_list = self.chunk(audio_path)
        console.print(f"↪ Chunk size: {len(audio_list)}", style="bold")

        transcriptions = []

        for audio in audio_list:
            console.print(f"\t↪ Transcribing {audio}...", style="bold")

            # Check if the transcript already exists
            transcript_path = f"{audio.split('.')[0]}.txt"
            if not os.path.exists(transcript_path):
                # Convert the MP3 file to text using Whisper API
                file = open(audio, "rb")
                response = openai.Audio.transcribe("whisper-1", file)

                # Check for errors in the API response
                if "error" in response:
                    error_msg = response["error"]["message"]
                    raise Exception(f"⚠️ Transcription error: {error_msg}")

                # Extract the transcript from the API response
                transcript = response["text"].strip()

                # Save the transcript to a text file
                with open(transcript_path, "w") as f:
                    f.write(transcript)
                    transcriptions.append(transcript)
                    console.print(
                        f"""
                    \t\t↪ saved transcript to {audio.split('.')[0]}.txt
                    (words: {len(transcript.split())}""",
                        style="bold"
                    )
            else:
                # Load the transcript from the text file
                with open(transcript_path, "r") as f:
                    transcriptions.append(f.read())
                pass

        full_transcript = " ".join(transcriptions)
        console.print(
            f"""↪ Total words: {len(full_transcript.split())}
            -- characters: {len(full_transcript)}""",
            style="bold"
        )

        return full_transcript, transcript_path

