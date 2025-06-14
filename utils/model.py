import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env (used locally; ignored on Railway)
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HF_TOKEN = os.getenv("HF_API_TOKEN")

# Ensure the token is available
if not HF_TOKEN:
    raise ValueError("Hugging Face API token not set. Please add HF_API_TOKEN in your .env or Railway environment variables.")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def classify_name(name):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": name})
        response.raise_for_status()  # Raise error for HTTP status 4xx/5xx
        result = response.json()[0][0]
        return {
            "label": result["label"],
            "confidence": round(result["score"] * 100, 2)
        }
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return {
            "label": "ERROR",
            "confidence": 0,
            "error": str(e)
        }
    except (KeyError, IndexError) as e:
        print(f"[ERROR] Unexpected response format: {response.text}")
        return {
            "label": "ERROR",
            "confidence": 0,
            "error": "Invalid API response format"
        }
