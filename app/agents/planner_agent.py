from app.core.config import get_settings
from app.models.schemas import ActionResponse, EmotionResponse

settings = get_settings()

class PlannerAgent:
    def __init__(self):
        if settings.USE_MOCK_LLM:
            self.client = None
        else:
            from app.services.ollama_service import OllamaService
            self.client = OllamaService()

    async def plan(self, emotion: EmotionResponse, weather: str, rag_actions: list) -> ActionResponse:
        if settings.USE_MOCK_LLM:
            # Return the first RAG suggestion or a default
            if rag_actions:
                best = rag_actions[0]
                return ActionResponse(
                    action=best.get('action', 'Breathe'),
                    description=best.get('description', 'Take a deep breath.'),
                    duration_minutes=best.get('duration_minutes', 1),
                    context_note=f"Selected from knowledge base for {emotion.emotion}."
                )
            return ActionResponse(
                action="Deep Breath",
                description="Take a deep breath in and out.",
                duration_minutes=1,
                context_note="Default mock action."
            )

        # Format RAG actions for the prompt
        rag_text = "\n".join([f"- {a['action']}: {a['description']}" for a in rag_actions])
        
        prompt = f"""You are a 'Mindful Moment' planner. Suggest ONE simple, effective micro-action (under 5 mins).
        
        Context:
        - User Emotion: {emotion.emotion}
        - Current Environment: {weather}
        - RAG Suggestions (Inspiration only):
        {rag_text}
        
        Instructions:
        1. Use the RAG suggestions as inspiration, but feel free to CREATE A NEW, UNIQUE ACTION if it fits the context better.
        2. VARY your suggestions. Do not always pick the first item.
        3. CRITICAL: Check the 'Current Environment'. If it is Raining, Snowy, or Nighttime, you MUST NOT suggest outdoor activities (like walking). In this case, politely acknowledge the user's intent but suggest an INDOOR alternative.
        4. Return JSON matching: {{"action": str, "description": str, "duration_minutes": int, "context_note": str}}
        """

        try:
            result = await self.client.generate_json(prompt)
            return ActionResponse(**result)
        except Exception as e:
            print(f"Error in Planner Agent: {e}")
            # Fallback
            return ActionResponse(
                action="Deep Breath",
                description="Take a deep breath in and out.",
                duration_minutes=1,
                context_note="Fallback due to error."
            )
