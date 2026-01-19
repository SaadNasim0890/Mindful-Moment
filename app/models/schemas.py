from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    text: str
    user_id: str = "default_user"
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class EmotionResponse(BaseModel):
    emotion: str
    confidence: float

class ActionResponse(BaseModel):
    action: str
    description: str
    duration_minutes: int
    context_note: str = ""

class FullAnalysisResponse(BaseModel):
    original_text: str
    detected_emotion: EmotionResponse
    suggested_action: ActionResponse
