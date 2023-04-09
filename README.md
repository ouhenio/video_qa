# Video Q&A

Video Q&A is a Command Line Interface (CLI) tool that allows you to interact with a large language model (LLM) agent to ask questions about a given YouTube video. It downloads the audio from the video, converts it to text using OPENAI's Whisper, and then feeds the text to an LLM to answer any questions you may have about the video content.

```console
python main.py --url https://www.youtube.com/watch?v=qCnaFLydb9c
```