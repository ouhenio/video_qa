import argparse
import cmd
import os

from dotenv import load_dotenv

from .llm import Agent
from .whisper import WhisperTranscriber
from .youtube import YouTubeDownloader


class VideoQA(cmd.Cmd):
    # ANSI escape codes for bold text
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    prompt = f"{bold_start}\nEnter your question: {bold_end}"

    def __init__(self, video_url):
        super().__init__()

        # Load environment variables from .env file
        os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv()

        # Get environment variables
        open_ai_key = os.getenv("OPENAI_API_KEY")

        downloader = YouTubeDownloader()
        print(f"About to download {video_url}")
        audio_path = downloader.download_video(video_url)
        print(f"Video saved at {audio_path}")

        transcriber = WhisperTranscriber(open_ai_key)
        transcript, transcript_path = transcriber.transcribe(audio_path)

        self.agent = Agent()
        self.agent.load_transcript(transcript_path=transcript_path)
        print(
            """
        You can now ask questions about the video.
        Type 'quit' or 'exit' to end the session.
        """
        )

    def default(self, line):
        if line.lower() in ["quit", "exit"]:
            return True

        print("\n" + "=" * 40 + "\n")
        agent_response = self.agent.query(line)
        print(f"🤖 : {agent_response}")
        print("\n" + "=" * 40)

    def do_EOF(self, line):
        print("Exiting...")
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interact with an LLM agent to ask questions about a YouTube video."
    )
    parser.add_argument("--url", required=True, help="YouTube video URL")

    args = parser.parse_args()

    VideoQA(args.url).cmdloop()
