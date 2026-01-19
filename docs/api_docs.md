# Mindful Moment Agent - API Reference

**Version:** 1.0.0
**Base URL:** `http://localhost:8000`

## Overview
The Mindful Moment API provides endpoints for emotion analysis, micro-action suggestions, and user history tracking. It is built with FastAPI and follows RESTful principles.

---

## Endpoints

### 1. Analyze Mood
**POST** `/analyze`

Analyzes the user's input text to detect their dominant emotion and suggests a personalized wellness micro-action.

#### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `text` | `string` | **Yes** | The user's input text describing their feelings. |
| `user_id` | `string` | No | Unique identifier for the user. Defaults to "default_user". |

**Example Request:**
```json
{
  "text": "I feel completely overwhelmed with my workload.",
  "user_id": "user_123"
}
```

#### Response (200 OK)
Returns a `FullAnalysisResponse` object.

| Field | Type | Description |
| :--- | :--- | :--- |
| `original_text` | `string` | The input text provided. |
| `detected_emotion` | `object` | Object containing emotion details. |
| `detected_emotion.emotion` | `string` | The classified emotion (e.g., "Stressed"). |
| `detected_emotion.confidence` | `float` | Confidence score (0.0 - 1.0). |
| `suggested_action` | `object` | Object containing the suggested action. |
| `suggested_action.action` | `string` | Title of the micro-action. |
| `suggested_action.description` | `string` | Detailed instructions. |
| `suggested_action.duration_minutes` | `integer` | Estimated time to complete. |

**Example Response:**
```json
{
  "original_text": "I feel completely overwhelmed with my workload.",
  "detected_emotion": {
    "emotion": "Stressed",
    "confidence": 0.98
  },
  "suggested_action": {
    "action": "One Thing Rule",
    "description": "Focus on just ONE task for the next 5 minutes.",
    "duration_minutes": 5,
    "context_note": "Selected for high stress context."
  }
}
```

#### Errors
| Status Code | Description |
| :--- | :--- |
| `422` | **Validation Error**: Missing required fields or invalid data types. |
| `500` | **Internal Server Error**: LLM or Database failure. |

---

### 2. Get History
**GET** `/history`

Retrieves the complete history of user interactions stored in the vector database.

#### Response (200 OK)
Returns an array of interaction objects.

**Example Response:**
```json
[
  {
    "content": "User felt Stressed (I feel overwhelmed...). Suggested: One Thing Rule.",
    "metadata": {
      "timestamp": "2023-12-09T14:30:00",
      "emotion": "Stressed",
      "action": "One Thing Rule"
    }
  }
]
```

---

### 3. Get Stats
**GET** `/stats`

Returns usage statistics for the system.

#### Response (200 OK)
**Example Response:**
```json
{
  "total_interactions": 42
}
```

---

## Models

### UserRequest
```json
{
  "text": "string",
  "user_id": "string"
}
```

### FullAnalysisResponse
```json
{
  "original_text": "string",
  "detected_emotion": {
    "emotion": "string",
    "confidence": 0.0
  },
  "suggested_action": {
    "action": "string",
    "description": "string",
    "duration_minutes": 0,
    "context_note": "string"
  }
}
```

---

## Authentication
The API is currently configured for **local development** and does not require authentication headers (e.g., Bearer tokens).
*   **Auth Type**: None
*   **Permissions**: Open access

---

## Global Status Codes
| Status Code | Description |
| :--- | :--- |
| 200 | **OK**: The request was successful. |
| 400 | **Bad Request**: The request was invalid (e.g., missing fields). |
| 422 | **Unprocessable Entity**: Validation error in the request body. |
| 500 | **Internal Server Error**: An unexpected error occurred on the server. |

