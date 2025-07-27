import chromadb
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class VectorMemory:
    def __init__(self, persist_directory="vector_db"):
        self.persist_directory = persist_directory
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            self.db = Chroma(
                collection_name="agent_memory",
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            print("✅ Vector store initialized successfully")
        except Exception as e:
            print(f"⚠️ Vector store initialization error: {e}")
            self.db = None

    def add(self, text, metadata=None):
        if self.db is None:
            print("⚠️ Vector store not available")
            return
        try:
            self.db.add_texts([text], metadatas=[metadata or {}])
            self.db.persist()
            print("✅ Added to vector memory")
        except Exception as e:
            print(f"⚠️ Error adding to vector store: {e}")

    def search(self, query, k=3):
        if self.db is None:
            print("⚠️ Vector store not available")
            return []
        try:
            results = self.db.similarity_search(query, k=k)
            print(f"🔍 Found {len(results)} related memories")
            return results
        except Exception as e:
            print(f"⚠️ Error searching vector store: {e}")
            return []