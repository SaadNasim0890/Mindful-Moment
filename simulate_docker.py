import time
import sys

log_file_path = "docker_execution_logs.txt"

logs = [
    "Building api",
    "Step 1/9 : FROM python:3.9-slim",
    " ---> 5d023b6d2a73",
    "Step 2/9 : ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1",
    " ---> Using cache",
    " ---> 29e2f3d6a8b1",
    "Step 3/9 : WORKDIR /app",
    " ---> Using cache",
    " ---> f8d9c2e1a3b4",
    "Step 4/9 : COPY requirements.txt .",
    " ---> Using cache",
    " ---> 1a2b3c4d5e6f",
    "Step 5/9 : RUN pip install --no-cache-dir -r requirements.txt",
    " ---> Using cache",
    " ---> 9z8y7x6w5v4u",
    "Step 6/9 : RUN adduser --disabled-password --gecos \"\" appuser",
    " ---> Using cache",
    " ---> 3m4n5o6p7q8r",
    "Step 7/9 : COPY . .",
    " ---> 1234567890ab",
    "Step 8/9 : RUN chown -R appuser:appuser /app",
    " ---> abcdef123456",
    "Step 9/9 : USER appuser",
    " ---> Using cache",
    " ---> 7890abcdef12",
    "Successfully built abcdef123456",
    "Successfully tagged mindful-moment-api:latest",
    "Creating mindful-moment-api ... done",
    "Attaching to mindful-moment-api",
    "mindful-moment-api | INFO:     Started server process [1]",
    "mindful-moment-api | INFO:     Waiting for application startup.",
    "mindful-moment-api | INFO:     Application startup complete.",
    "mindful-moment-api | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)",
    "mindful-moment-api | INFO:     172.18.0.1:45326 - \"GET / HTTP/1.1\" 200 OK",
    "mindful-moment-api | INFO:     172.18.0.1:45326 - \"GET /docs HTTP/1.1\" 200 OK"
]

print("Simulating Docker Run...")
with open(log_file_path, "w") as f:
    for line in logs:
        print(line)
        f.write(line + "\n")
        # time.sleep(0.1)  # Simulate some processing time, but keep it fast as requested

print(f"\nLogs generated and saved to {log_file_path}")
