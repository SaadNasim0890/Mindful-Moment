import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app.api.main import app, startup_event
    print("Successfully imported app.api.main")
    
    import asyncio
    print("Running startup_event...")
    asyncio.run(startup_event())
    print("Startup event completed successfully.")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
