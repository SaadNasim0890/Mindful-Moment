@echo off
echo ===================================================
echo      Mindful Moment AI - Real AI Mode (Llama 3)
echo ===================================================
echo.
echo Starting Server...
echo The browser will open automatically.
echo.

:: Open browser in background
start "" "http://localhost:8000"

:: Start the FastAPI server
uvicorn app.api.main:app --host 0.0.0.0 --port 8000

pause
