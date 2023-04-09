# Video Q&A Agent

Video Q&A Agent is a Command Line Interface (CLI) tool that allows you to interact with ChatGPT and ask questions about a given YouTube video. It downloads the audio from the video, converts it to text using OpenAI's Whisper, and then feeds the text to an LLM to answer any questions you may have about the video content.

## Installation

```console
pip install -r requirements/base.txt
```

**Note**: You need to setup a `.env` file with your OpenAI keys. See `.env.example` for a reference.

**Optional**: If you want to run whisper locally, you'll require to install `openai-whisper`:

```console
pip install openai-whisper
```

## Usage

```console
python -m video_qa --url "https://www.youtube.com/watch?v=X29p13cAT1g"
```

Example outputs:

```
You can now ask questions about the video. Type 'quit' or 'exit' to end the session.
About to download https://www.youtube.com/watch?v=X29p13cAT1g
Audio file already exists: downloads/X29p13cAT1g.mp3
Video saved at downloads/X29p13cAT1g.mp3
🗣️  Initializing Whisper transcriber...
↪ 💵 Estimated cost: $0.02 (3.19 minutes)
↪ Chunk size: 1
	↪ Transcribing downloads/X29p13cAT1g.mp3...
↪ Total words: 453 -- characters: 2338
Using embedded DuckDB without persistence: data will be transient

Enter your question: what is the video about?

========================================

🤖 : The video transcript does not provide a clear answer as it contains multiple discussions. However, one section of the video discusses the pricing of concert tickets and how much money the band makes from ticket sales.

========================================

Enter your question: what do they say about the concert prices?

========================================

🤖 : They discuss the high cost of production and the fact that the band often makes the least amount of money. They mention that they charge around $17 to $18 per ticket and only see about 25% of that, which they then have to split three ways and pay taxes on. They also mention other artists who charge much higher prices for tickets.

========================================

```
