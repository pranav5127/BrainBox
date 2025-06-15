from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY
from langchain_huggingface import HuggingFaceEmbeddings

import os

"""
Gemini RAG (Retrieval Augmented Generation) Service

This module provides an interface to Google's Gemini model combined with vector-based retrieval 
to answer questions over a given document corpus.

The `GeminiRAGService` class loads documents, splits them into chunks, generates embeddings, 
stores them in a FAISS vectorstore, and queries them using Google's Gemini model via LangChain.

Classes:
    - GeminiRAGService: Full end-to-end RAG system powered by Gemini and FAISS.

Functions:
    - __init__(file_path, embedding_model): Initializes document loading, embedding, FAISS storage, retriever, and Gemini model.
    - get_answer(query): Answers a user query using RAG pipeline.

Usage:
    service = GeminiRAGService("/path/to/file.txt")
    reply = service.get_answer("Explain the document.")

Parameters:
    - file_path (str): The path to the document file to load and process.
    - embedding_model (str): Optional. The HuggingFace model to use for embeddings (default: "sentence-transformers/all-MiniLM-L6-v2").

Returns:
    - str: The generated answer based on the provided query and document content.

Configuration:
    The Gemini API key must be provided via `GEMINI_API_KEY` in the config module (`utils.config`).

Note:
    - This implementation uses FAISS for local vector storage.
    - Document is chunked before embedding for better retrieval performance.
    - Extend the class to load multiple files or add persistence to FAISS if required.
"""


class GeminiRAGService:
    def __init__(self, file_path: str, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

        self.file_path = file_path
        self.embedding_model = embedding_model

        # Load and process documents
        self.docs = self.load_documents()
        self.chunks = self.split_documents()

        # Embedding and vector store
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        self.db = FAISS.from_documents(self.chunks, self.embeddings)

        # Retriever and LLM
        self.retriever = self.db.as_retriever()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever
        )

    def load_documents(self):
        loader = TextLoader(self.file_path)
        return loader.load()

    def split_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_documents(self.docs)

    def get_answer(self, query: str) -> str:
        """
        Get answer from RAG system for the provided query.
        """
        result = self.qa_chain.invoke(query)
        return result['result']


if __name__ == "__main__":
    service = GeminiRAGService(
        file_path="/home/pranav/PycharmProjects/PythonProject/adk_prototype/presentation_agent/pdfs/earth.txt"
    )

    query = "Tell me something about this text!"
    answer = service.get_answer(query)

    print("\n=== Answer ===")
    print(answer)
