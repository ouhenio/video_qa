from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

class Agent:
    def __init__(self) -> None:
        self.chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        self.docsearch = None
        pass

    def load_transcript(self, transcript_path):
        index_creator = VectorstoreIndexCreator()
        loader = TextLoader(transcript_path)
        self.docsearch = index_creator.from_loaders([loader])
    
    def query(self, query):
        docs = self.docsearch.vectorstore.similarity_search(query)
        output = self.chain.run(input_documents=docs, question=query)

        return output