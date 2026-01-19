# Engineering Report: Mindful Moment Agent

**Date:** December 9, 2025
**Project:** Mindful Moment AI Companion

## 1. Executive Summary
The Mindful Moment Agent is a privacy-first, local AI application designed to provide real-time emotional support and wellness micro-actions. By leveraging a local Large Language Model (Llama 3.2) and a Retrieval-Augmented Generation (RAG) architecture, the system offers personalized advice without sending sensitive user data to the cloud. This report details the system architecture, key engineering challenges, and final implementation results.

## 2. System Architecture

### 2.1 High-Level Design
The system follows a modular micro-agent architecture orchestrated by a FastAPI backend.
*   **Frontend**: A lightweight, responsive HTML/CSS/JS client using a "Glassmorphism" design language.
*   **Backend**: Python FastAPI server handling request routing and agent orchestration.
*   **Intelligence Layer**: 
    *   **Ollama**: Hosts the Llama 3.2 (1B/3B) model for local inference.
    *   **FAISS**: A vector database for efficient similarity search (RAG) and history persistence.

### 2.2 Core Components
*   **Emotion Agent**: Uses few-shot prompting to classify user text into 9 distinct emotional states (e.g., Stressed, Anxious, Bored).
*   **RAG Service**: Retrieves relevant wellness techniques from a curated knowledge base of 572 micro-actions.
*   **Planner Agent**: Synthesizes the detected emotion, retrieved actions, and environmental context (Time/Weather) to generate a final, actionable suggestion.
*   **Tracking Agent**: Asynchronously logs interactions to the FAISS vector store for long-term memory.

## 3. Engineering Challenges & Solutions

### 3.1 Local LLM Integration
**Challenge**: Integrating `langchain-community` with the local Ollama instance caused compatibility issues (`TypeError: unhashable type: 'list'`) due to library version conflicts in the Python 3.9 environment.
**Solution**: We implemented a custom `OllamaService` using the `httpx` library. This lightweight client interacts directly with the Ollama API endpoints, bypassing the abstraction layer overhead and resolving the stability issues while maintaining full control over the prompt structure.

### 3.2 Data Scarcity & Repetition
**Challenge**: The initial knowledge base contained only 7 actions, leading to repetitive suggestions that degraded user experience.
**Solution**: We developed a procedural generation script (`generate_data.py`) that algorithmically created **572 unique micro-actions**. The script used templates tailored to specific emotions and applied variations in duration, description, and intensity to ensure a diverse and robust dataset.

### 3.3 Persistence & Privacy
**Challenge**: Storing user history without a heavy database server (like PostgreSQL) while enabling semantic search.
**Solution**: We utilized **FAISS (Facebook AI Similarity Search)** as a dual-purpose store. It functions as both the RAG knowledge base and the history logger. This allows the system to remain entirely local (file-based persistence) and enables future features like "finding past moments similar to now."

## 4. Results & Performance

### 4.1 Functionality
The system successfully handles the full user flow:
1.  **Input**: User expresses complex feelings (e.g., "I'm anxious about my deadline").
2.  **Analysis**: System correctly identifies "Anxious" (Confidence > 0.9).
3.  **Retrieval**: System fetches grounding techniques from the 500+ item database.
4.  **Response**: System suggests "Texture Touch" or "Double Exhale" within 2-3 seconds.

### 4.2 Reliability
*   **Uptime**: The FastAPI server runs stably with automated recovery handled by the `run_app.bat` script.
*   **Error Handling**: Fallback mechanisms are in place; if the LLM fails, the system defaults to rule-based suggestions to ensure the user always receives support.

## 5. Future Work
*   **Voice Interface**: Adding Speech-to-Text (Whisper) for hands-free interaction.
*   **Biometric Integration**: Connecting to wearables (Fitbit/Apple Watch) to detect stress via Heart Rate Variability (HRV).
*   **Long-term Trends**: Visualizing mood trends over weeks/months on the History page.

## 6. Conclusion
The Mindful Moment Agent demonstrates the viability of powerful, local-first AI applications. By combining efficient engineering (FastAPI, FAISS) with capable local models (Llama 3), we have delivered a product that is both intelligent and strictly private.
