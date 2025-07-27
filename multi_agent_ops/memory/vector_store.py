import chromadb
import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class VectorMemory:
    def __init__(self, persist_directory="vector_db"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.db = Chroma(
            collection_name="agent_memory",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add(self, text, metadata=None):
        self.db.add_texts([text], metadatas=[metadata or {}])
        self.db.persist()

    def search(self, query, k=3):
        return self.db.similarity_search(query, k=k)
