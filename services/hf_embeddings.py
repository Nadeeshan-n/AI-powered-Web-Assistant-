from typing import List

from huggingface_hub import InferenceClient
from langchain_core.embeddings import Embeddings

from config import HF_TOKEN, HF_EMBEDDING_MODEL


class HuggingFaceEmbeddings(Embeddings):
    """
    LangChain-compatible embeddings using
    Hugging Face Inference Providers.
    """

    def __init__(self):
        if not HF_TOKEN:
            raise ValueError(
                "HF_TOKEN is not configured in .env"
            )

        self.client = InferenceClient(
            provider="hf-inference",
            api_key=HF_TOKEN,
        )

    def embed_documents(
        self,
        texts: List[str]
    ) -> List[List[float]]:

        result = self.client.feature_extraction(
            texts,
            model=HF_EMBEDDING_MODEL,
        )

        return result.tolist()

    def embed_query(
        self,
        text: str
    ) -> List[float]:

        result = self.client.feature_extraction(
            text,
            model=HF_EMBEDDING_MODEL,
        )

        return result.tolist()