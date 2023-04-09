import argparse
import cmd
import os

from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.panel import Panel

from .llm import Agent
from .whisper.openai import WhisperTranscriber
from .youtube import YouTubeDownloader


class VideoQA(cmd.Cmd):
    console = Console()
    prompt = "Enter your question: "

    def __init__(self, video_url, whisper_model=None, use_local_whisper=False):
        super().__init__()

        # Load environment variables from .env file
        os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv()

        # Get environment variables
        open_ai_key = os.getenv("OPENAI_API_KEY")

        downloader = YouTubeDownloader()
        self.console.print(f"About to download {video_url}", style="bold")
        audio_path = downloader.download_video(video_url)
        self.console.print(f"Video saved at {audio_path}", style="bold")

        if use_local_whisper:
            from .whisper.local import LocalWhisperTranscriber

            self.console.print("Using a local version of whisper.", style="bold")
            transcriber = LocalWhisperTranscriber(whisper_model)
        else:
            transcriber = WhisperTranscriber(open_ai_key)
        transcript, transcript_path = transcriber.transcribe(audio_path)

        self.agent = Agent()
        self.agent.load_transcript(transcript_path=transcript_path)
        self.console.print(
            Panel(
                """
        You can now ask questions about the video.
        Type 'quit' or 'exit' to end the session.
        """,
                title="Instructions",
                expand=False,
            )
        )

    def default(self, line):
        if line.lower() in ["quit", "exit"]:
            return True

        self.console.print("\n" + "=" * 40 + "\n")
        agent_response = self.agent.query(line)
        self.console.print(f"🤖 : {agent_response}", style="bold")
        self.console.print("\n" + "=" * 40)

    def do_EOF(self, line):
        self.console.print("Exiting...", style="bold")
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interact with an LLM agent to ask questions about a YouTube video."
    )
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument(
        "--use-local-whisper",
        action="store_true",
        help="Use local version of Whisper instead of OpenAI API",
    )
    parser.add_argument(
        "--whisper-model",
        default="base",
        help="Specify the Whisper model version to use (default: base)",
    )

    args = parser.parse_args()

    VideoQA(
        args.url,
        use_local_whisper=args.use_local_whisper,
        whisper_model=args.whisper_model,
    ).cmdloop()
