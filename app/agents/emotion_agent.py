from app.core.config import get_settings
from app.models.schemas import EmotionResponse

settings = get_settings()

class EmotionAgent:
    def __init__(self):
        if settings.USE_MOCK_LLM:
            self.client = None
        else:
            from app.services.ollama_service import OllamaService
            self.client = OllamaService()

    async def analyze(self, text: str) -> EmotionResponse:
        if settings.USE_MOCK_LLM:
            # Simple keyword matching for demo
            text_lower = text.lower()
            if "tired" in text_lower or "sleep" in text_lower or "exhausted" in text_lower:
                return EmotionResponse(emotion="Tired", confidence=0.9)
            elif "sad" in text_lower or "cry" in text_lower or "hopeless" in text_lower or "blue" in text_lower:
                return EmotionResponse(emotion="Sad", confidence=0.9)
            elif "happy" in text_lower or "good" in text_lower or "wonderful" in text_lower or "best" in text_lower:
                return EmotionResponse(emotion="Happy", confidence=0.9)
            elif "confused" in text_lower or "lost" in text_lower or "foggy" in text_lower or "sure" in text_lower:
                return EmotionResponse(emotion="Confused", confidence=0.8)
            elif "anxious" in text_lower or "nervous" in text_lower or "racing" in text_lower:
                return EmotionResponse(emotion="Anxious", confidence=0.85)
            elif "angry" in text_lower or "mad" in text_lower or "frustrat" in text_lower:
                return EmotionResponse(emotion="Angry", confidence=0.85)
            elif "ored" in text_lower: # bored
                return EmotionResponse(emotion="Bored", confidence=0.8)
            elif "overwhelmed" in text_lower or "drowning" in text_lower:
                return EmotionResponse(emotion="Overwhelmed", confidence=0.9)
            else:
                return EmotionResponse(emotion="Stressed", confidence=0.85)

        prompt = f"""You are an expert AI psychologist. Your task is to accurately classify the user's dominant emotion.
        
        Available Categories:
        - Stressed (pressure, overwhelmed, busy)
        - Tired (exhausted, sleepy, drained)
        - Sad (down, unhappy, grief)
        - Confused (uncertain, lost, brain fog)
        - Happy (joyful, excited, grateful)
        - Anxious (nervous, worried, panic)
        - Angry (mad, frustrated, annoyed)
        - Bored (uninterested, dull)
        - Overwhelmed (too much to do, drowning)

        User Text: "{text}"

        Instructions:
        1. Analyze the nuance of the text.
        2. Select the MOST fitting category from the list above.
        3. Return ONLY a JSON object. Do not add any other text.
        
        Examples:
        - "I have so much to do and not enough time." -> {{"emotion": "Stressed", "confidence": 0.95}}
        - "I just want to crawl into bed." -> {{"emotion": "Tired", "confidence": 0.9}}
        - "I don't know why I feel this way." -> {{"emotion": "Confused", "confidence": 0.8}}
        
        Output Format:
        {{"emotion": "CategoryName", "confidence": 0.0-1.0}}
        """

        try:
            result = await self.client.generate_json(prompt)
            return EmotionResponse(**result)
        except Exception as e:
            print(f"Error in Emotion Agent: {e}")
            return EmotionResponse(emotion="Stressed", confidence=0.0)
