import requests
from abc import ABC
from typing import List
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.llms.base import LLM


class LlamaLLM(LLM, ABC):
    def __init__(self, api_url: str, model: str):
        super().__init__()
        self._api_url = api_url
        self._model = model

    @property
    def _llm_type(self) -> str:
        return "llama"

    def _call(self, prompt: str, stop: List[str] = None) -> str:
        """Query Meta's Llama model via Ollama."""
        response = requests.post(
            f"{self._api_url}/generate",
            json={"model": self._model, "prompt": prompt, "stream": False}
        )
        if response.status_code != 200:
            raise RuntimeError(f"Failed to generate response: {response.text}")
        return response.json()["response"]


class KnowledgeBase:
    def __init__(self, texts: List[str], embeddings: Embeddings):
        self.vector_store = FAISS.from_texts(texts, embeddings)

    def get_retriever(self):
        return self.vector_store.as_retriever()


class LlamaRetrievalQA:
    def __init__(self, llm: LLM, knowledge_base: KnowledgeBase):
        self.retriever = knowledge_base.get_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=self.retriever)

    def query(self, question: str) -> str:
        return self.qa_chain.invoke(question)
