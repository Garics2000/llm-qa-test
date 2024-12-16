import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS

from ...chatbot.embeddings import LlamaEmbeddings
from ...chatbot.llm import LlamaLLM



class RetrievalQAHelper:
    """Helper class to init RetrievalQA chain with the given knowledge base."""
    def __init__(self, knowledge_base: dict):
        self.knowledge_base = knowledge_base
        self.retriever = self._initialize_retriever()
        self.qa_chain = self._initialize_qa_chain()

    def _initialize_retriever(self):
        texts = list(self.knowledge_base.values())
        embedder = LlamaEmbeddings(
            api_url=os.getenv("LLM_API_URL"),
            model=os.getenv("LLM_MODEL", "llama3.2")
        )

        # Embed documents using LlamaEmbeddings
        embeddings = embedder.embed_documents(texts)

        # Pair embeddings with texts
        text_embeddings = list(zip(texts, embeddings))

        # Initialize FAISS with text-embedding pairs
        vector_store = FAISS.from_embeddings(
            text_embeddings=text_embeddings,
            embedding=embedder.embed_query
        )
        return vector_store.as_retriever()

    def _initialize_qa_chain(self):
        return RetrievalQA.from_chain_type(
            llm=LlamaLLM(
                api_url=os.getenv("LLM_API_URL"),
                model=os.getenv("LLM_MODEL", "llama3.2")
            ),
            retriever=self.retriever
        )

    def query(self, question: str) -> str:
        return self.qa_chain.run(question)
