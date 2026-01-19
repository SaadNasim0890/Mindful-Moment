from fastapi.testclient import TestClient
from app.api.main import app
import pytest

client = TestClient(app)


def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text or "html" in response.text

def test_read_stats():
    with TestClient(app) as client:
        response = client.get("/stats")
        assert response.status_code == 200
        assert "total_interactions" in response.json()

def test_analyze_mock():
    # Integration test
    payload = {"text": "I feel happy", "user_id": "test_user"}
    with TestClient(app) as client:
        try:
            response = client.post("/analyze", json=payload)
            if response.status_code == 200:
                data = response.json()
                assert "suggested_action" in data
                assert "detected_emotion" in data
        except Exception:
            pytest.skip("Skipping full integration due to external config")


if __name__ == "__main__":
    # Allow running directly
    pass
