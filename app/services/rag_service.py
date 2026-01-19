import json
from app.core.config import get_settings
from typing import List, Dict

settings = get_settings()

class RAGService:
    def __init__(self):
        if settings.USE_MOCK_LLM:
            self.db = None
            return

        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        try:
            self.db = FAISS.load_local("data/faiss_rag", self.embeddings, allow_dangerous_deserialization=True)
        except:
            self.db = None
            self._initialize_data()

    def _initialize_data(self):
        from langchain_community.vectorstores import FAISS
        import json
        
        try:
            with open("data/micro_actions.json", "r") as f:
                actions = json.load(f)
            
            texts = [f"{a['emotion']}: {a['action']} - {a['description']}" for a in actions]
            metadatas = actions
            
            self.db = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
            self.db.save_local("data/faiss_rag")
            print(f"Ingested {len(actions)} actions into FAISS.")
        except Exception as e:
            print(f"Error initializing RAG data: {e}")

    def query_actions(self, emotion: str, n_results: int = 3) -> list:
        if settings.USE_MOCK_LLM:
            # Return dummy actions
            return [{
                "action": "Mock Action",
                "description": "This is a mock action because database is disabled.",
                "duration_minutes": 5,
                "emotion": emotion
            }]

        if not self.db:
            return []

        docs = self.db.similarity_search(emotion, k=n_results)
        return [d.metadata for d in docs]
