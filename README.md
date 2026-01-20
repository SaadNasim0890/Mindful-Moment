# Mindful Moment AI

Mindful Moment AI is an intelligent mental wellness application designed to provide real-time emotional analysis and personalized action planning. By leveraging advanced NLP models and contextual data, it helps users understand their emotions and take meaningful steps towards better mental health.

## 🚀 Key Features

*   **Real-time Emotion Detection**: Utilizes a specialized `EmotionAgent` to accurately identify user emotions from text input.
*   **Context-Aware Action Planning**: The `PlannerAgent` combines emotional triggers with real-time weather data (`WeatherService`) and user history to suggest tailored micro-actions.
*   **RAG-Powered Suggestions**: A Retrieval-Augmented Generation (RAG) system (`RAGService`) queries a vector database of over 500 micro-actions to provide scientifically backed recommendations.
*   **Progress Tracking**: The `TrackingAgent` logs interactions and generates visual analytics to track mood trends and action effectiveness over time.
*   **Modern Web Interface**: A clean, responsive UI built with FastAPI and static HTML/JS for seamless interaction.

## 🛠️ Technology Stack

*   **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python web framework)
*   **AI/LLM Logic**: [LangChain](https://python.langchain.com/) (Orchestration of agents and chains)
*   **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local storage for RAG embeddings)
*   **Deployment**: Docker & Docker Compose
*   **Testing**: Pytest

## 📦 Installation

### Prerequisites
*   Python 3.10+
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Optional, for containerized run)

### Setup via pip

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/mindful-moment.git
    cd mindful-moment
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Linux/Mac
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment:
    Create a `.env` file in the root directory (see `.env.example`) and add your API keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    WEATHER_API_KEY=your_weather_api_key
    ```

## 🎮 Usage

### Quick Start (Windows)
Simply run the provided batch script to start the server and open the browser automatically:
```bash
run_app.bat
```

### Manual Start
Start the Uvicorn server directly:
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser to `http://localhost:8000`.

### Docker Run
To run the entire application in a container:
```bash
docker-compose up --build
```

## 📂 Project Structure

```
mindful-moment/
├── app/
│   ├── agents/         # Core logic for Emotion, Planner, and Tracking agents
│   ├── api/            # FastAPI endpoints (main.py)
│   ├── core/           # Configuration and settings
│   ├── models/         # Pydantic data models
│   ├── services/       # External services (RAG, Weather)
│   └── static/         # Frontend assets (HTML, JS, CSS)
├── data/               # JSON datasets and ChromaDB storage
├── docs/               # Project documentation and reports
├── tests/              # Automated test suite
├── docker-compose.yml  # Docker container config
└── requirements.txt    # Python dependencies
```

## 🧪 Testing

Run the automated test suite to verify system integrity:
```bash
pytest tests/
```

## 📄 Documentation

Detailed engineering reports and test results can be found in the `docs/` directory:
*   [Engineering Report](docs/engineering_report.html)
*   [Test Report](docs/test_report.md)
