from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma

from services.hf_embeddings import HuggingFaceEmbeddings


DOCUMENTS_DIR = Path("data/documents")
VECTORSTORE_DIR = Path("vectorstore")

COLLECTION_NAME = "knowledge_base"


class RAGService:

    def __init__(self):

        DOCUMENTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        VECTORSTORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.embeddings = HuggingFaceEmbeddings()

        self.vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=str(VECTORSTORE_DIR),
            embedding_function=self.embeddings,
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    # --------------------------------------------------------
    # Load PDF
    # --------------------------------------------------------

    def load_pdf(
        self,
        file_path: str
    ) -> List[Document]:

        loader = PyPDFLoader(file_path)

        return loader.load()

    # --------------------------------------------------------
    # Split documents
    # --------------------------------------------------------

    def split_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:

        return self.text_splitter.split_documents(
            documents
        )

    # --------------------------------------------------------
    # Index PDF
    # --------------------------------------------------------

    def index_pdf(
        self,
        file_path: str
    ) -> int:

        documents = self.load_pdf(
            file_path
        )

        chunks = self.split_documents(
            documents
        )

        self.vectorstore.add_documents(
            chunks
        )

        return len(chunks)

    # --------------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------------

    def retrieve(
        self,
        query: str,
        k: int = 4
    ) -> List[Document]:

        return self.vectorstore.similarity_search(
            query,
            k=k
        )

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    def build_context(
        self,
        documents: List[Document]
    ) -> str:

        if not documents:
            return "No relevant knowledge was found."

        context_parts = []

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown"
            )

            page = document.metadata.get(
                "page",
                "Unknown"
            )

            # Convert page number to human-friendly numbering
            if isinstance(page, int):
                page = page + 1

            context_parts.append(
                f"Source: {source}\n"
                f"Page: {page}\n"
                f"Content:\n"
                f"{document.page_content}"
            )

        return "\n\n---\n\n".join(
            context_parts
        )

    # --------------------------------------------------------
    # Extract source information
    # --------------------------------------------------------

    def get_sources(
        self,
        documents: List[Document]
    ) -> list:

        sources = []

        for document in documents:

            source = document.metadata.get(
                "source",
                "Unknown"
            )

            page = document.metadata.get(
                "page",
                "Unknown"
            )

            if isinstance(page, int):
                page = page + 1

            sources.append({
                "document": Path(
                    source
                ).name,
                "page": page,
            })

        return sources


rag_service = RAGService()