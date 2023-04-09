from video_qa.whisper import WhisperTranscriber
from video_qa.youtube import YouTubeDownloader
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    # Load environment variables from .env file
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv()

    # Get environment variables
    open_ai_key = os.getenv('OPENAI_API_KEY')


    video_url = "https://www.youtube.com/watch?v=qCnaFLydb9c"
    downloader = YouTubeDownloader()
    print(f"About to download {video_url}")
    audio_path = downloader.download_video(video_url)
    print(f"Video saved at {audio_path}")
    
    transcriber = WhisperTranscriber(open_ai_key)
    transcript, transcript_path = transcriber.transcribe(audio_path)

    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.vectorstores import Chroma
    from langchain.docstore.document import Document
    from langchain.prompts import PromptTemplate
    from langchain.indexes.vectorstore import VectorstoreIndexCreator
    from langchain.document_loaders import TextLoader
    from langchain.chains.question_answering import load_qa_chain
    from langchain.llms import OpenAI

    index_creator = VectorstoreIndexCreator()
    loader = TextLoader(transcript_path)
    docsearch = index_creator.from_loaders([loader])

    query = "they mentioned a music concert, who it was from?"
    docs = docsearch.vectorstore.similarity_search(query)
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    query = "they mentioned a music concert, who it was from?"
    output = chain.run(input_documents=docs, question=query)
    print(output)

