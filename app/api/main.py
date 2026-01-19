from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import get_settings
from app.models.schemas import UserRequest, FullAnalysisResponse
from app.agents.emotion_agent import EmotionAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.tracking_agent import TrackingAgent
from app.services.rag_service import RAGService
from app.services.weather_service import WeatherService

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Global instances (in a real app, use dependency injection)
emotion_agent = None
planner_agent = None
tracking_agent = None
rag_service = None
weather_service = None

@app.on_event("startup")
async def startup_event():
    global emotion_agent, planner_agent, tracking_agent, rag_service, weather_service
    emotion_agent = EmotionAgent()
    planner_agent = PlannerAgent()
    tracking_agent = TrackingAgent()
    rag_service = RAGService()
    weather_service = WeatherService()

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')

@app.get("/view-history")
async def view_history_page():
    return FileResponse('app/static/history.html')

@app.post("/analyze", response_model=FullAnalysisResponse)
async def analyze_mood(request: UserRequest, background_tasks: BackgroundTasks):
    try:
        # 1. Analyze Emotion
        emotion_response = await emotion_agent.analyze(request.text)
        
        # 2. Get Context (Parallelizable in theory, sequential here for simplicity)
        weather_context = await weather_service.get_current_context(request.latitude, request.longitude)
        rag_suggestions = rag_service.query_actions(emotion_response.emotion)
        
        # 3. Plan Action
        action_response = await planner_agent.plan(
            emotion=emotion_response,
            weather=weather_context,
            rag_actions=rag_suggestions
        )
        
        # 4. Construct Response
        full_response = FullAnalysisResponse(
            original_text=request.text,
            detected_emotion=emotion_response,
            suggested_action=action_response
        )
        
        # 5. Log Interaction (Background Task)
        background_tasks.add_task(tracking_agent.log_interaction, full_response)
        
        return full_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    return tracking_agent.get_stats()

@app.get("/history")
async def get_history():
    return tracking_agent.get_history()
