from whisper import WhisperTranscriber
from youtube import YouTubeDownloader
from llm import Agent
from dotenv import load_dotenv
import os
import argparse

def main(video_url):
    # Load environment variables from .env file
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv()

    # Get environment variables
    open_ai_key = os.getenv('OPENAI_API_KEY')

    downloader = YouTubeDownloader()
    print(f"About to download {video_url}")
    audio_path = downloader.download_video(video_url)
    print(f"Video saved at {audio_path}")

    transcriber = WhisperTranscriber(open_ai_key)
    transcript, transcript_path = transcriber.transcribe(audio_path)

    agent = Agent()
    agent.load_transcript(transcript_path=transcript_path)

    print("You can now ask questions about the video. Type 'quit' or 'exit' to end the session.")
    while True:
        user_input = input("Enter your question: ")

        if user_input.lower() in ['quit', 'exit']:
            break

        agent_response = agent.query(user_input)
        print(agent_response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interact with an LLM agent to ask questions about a YouTube video.")
    parser.add_argument('--url', required=True, help="YouTube video URL")

    args = parser.parse_args()
    main(args.url)

