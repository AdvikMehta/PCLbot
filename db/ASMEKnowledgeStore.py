from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

class ASMEKnowledgeStore:

    def __init__(self, index_name: str, init_doc_paths: list = None):
        load_dotenv()
        self.index_name = index_name
        self.embeddings = OpenAIEmbeddings()

        if init_doc_paths is not None:
            self.vectordb = self.__init_index_with_docs(
                self.index_name,
                self.embeddings,
                init_doc_paths,
            )
        else:
            self.vectordb = Pinecone.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings
            )

    def similarity_search(self, query: str):
        """
        Performs a similarity search on the Vector Database and returns the top match
        TODO: refactor for returning top k matches
        """
        docs = self.vectordb.similarity_search(query)
        return docs[0].page_content

    def __init_index_with_docs(self, index_name, embeddings, init_doc_paths) -> VectorStore:
        """
        Initializes a Pinecone index with input PDF docs
        """
        return PineconeVectorStore.from_documents(
            self.__process_pdfs(init_doc_paths),
            embeddings,
            index_name=index_name)

    def __process_pdfs(self, init_doc_paths) -> list[Document]:
        """
        Processs PDFs - loads and splits documents
        """
        docs = []
        for path in init_doc_paths:
            # init loader and load data
            loader = PyPDFLoader(path)
            data = loader.load()

            # split into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs += text_splitter.split_documents(data)

        return docs

