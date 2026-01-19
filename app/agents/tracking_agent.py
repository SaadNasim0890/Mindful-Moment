from app.core.config import get_settings
from app.models.schemas import FullAnalysisResponse
import uuid
from datetime import datetime

settings = get_settings()

class TrackingAgent:
    def __init__(self):
        if settings.USE_MOCK_LLM:
            self.db = None
            return

        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        try:
            self.db = FAISS.load_local("data/faiss_history", self.embeddings, allow_dangerous_deserialization=True)
        except:
            # Initialize empty
            self.db = FAISS.from_texts(["Initial Log"], self.embeddings, metadatas=[{"timestamp": "init"}])
            self.db.save_local("data/faiss_history")

    async def log_interaction(self, response: FullAnalysisResponse):
        if settings.USE_MOCK_LLM:
            print(f"Mock Log: {response.detected_emotion.emotion} -> {response.suggested_action.action}")
            return

        try:
            document = f"User felt {response.detected_emotion.emotion} ({response.original_text}). Suggested: {response.suggested_action.action}."
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "emotion": response.detected_emotion.emotion,
                "action": response.suggested_action.action
            }
            
            self.db.add_texts([document], metadatas=[metadata])
            self.db.save_local("data/faiss_history")
        except Exception as e:
            print(f"Error logging interaction: {e}")

    def get_stats(self):
        if settings.USE_MOCK_LLM:
            return {"total_interactions": 999, "note": "Mock Mode"}
            
        return {
            "total_interactions": self.db.index.ntotal
        }

    def get_history(self):
        if settings.USE_MOCK_LLM:
            return [{"timestamp": "mock", "emotion": "mock", "action": "mock"}]
            
        try:
            # Access the underlying docstore to get all documents
            docs = self.db.docstore._dict.values()
            history = []
            for doc in docs:
                history.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            # Sort by timestamp descending if possible
            history.sort(key=lambda x: x['metadata'].get('timestamp', ''), reverse=True)
            return history
        except Exception as e:
            return {"error": str(e)}
