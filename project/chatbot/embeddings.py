import requests
from typing import List
from langchain.embeddings.base import Embeddings


class LlamaEmbeddings(Embeddings):
    def __init__(self, api_url: str, model: str):
        self.api_url = api_url
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents using Llama's API."""
        response = requests.post(
            f"{self.api_url}/embed",
            json={"model": self.model, "input": texts}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Failed to embed documents: {response.text}")
        return response.json()["embeddings"]

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query using Llama's API."""
        response = requests.post(
            f"{self.api_url}/embed",
            json={"model": self.model, "input": [text]}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Failed to embed query: {response.text}")
        return response.json()["embeddings"][0]