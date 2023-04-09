from chromadb.errors import NotEnoughElementsException
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator


class Agent:
    def __init__(self) -> None:
        self.docsearch = None
        self.template = """
        You are a bot that consumes transcripts of youtube videos,
        and answers questions of its content.

        Your answers should be helpful, consise, and factual.

        Video transcript: {context}

        User question: {question}
        """
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"], template=self.template
        )
        self.chain = load_qa_chain(
            ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
            chain_type="stuff",
            prompt=self.prompt_template,
        )

    def load_transcript(self, transcript_path):
        index_creator = VectorstoreIndexCreator()
        loader = TextLoader(transcript_path)
        self.docsearch = index_creator.from_loaders([loader])

    def query(self, query):
        try:
            docs = self.docsearch.vectorstore.similarity_search(query)
        except NotEnoughElementsException:
            # If there are fewer elements in the index than 4, return 3.
            docs = self.docsearch.vectorstore.similarity_search(query, k=3)

        output = self.chain.run(input_documents=docs, question=query)

        return output
