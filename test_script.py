import requests
import json

def test_analyze():
    url = "http://localhost:8000/analyze"
    payload = {
        "text": "I am feeling very overwhelmed with all the work I have to do."
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_analyze()
