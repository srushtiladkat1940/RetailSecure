import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HF_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_TOKEN:
    raise ValueError("Hugging Face API token not set. Please add HF_API_TOKEN in your .env or Railway environment variables.")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def classify_name(name):
    if not name or name.strip().lower() in ["unknown product", "error fetching product"]:
        return {
            "label": "ERROR",
            "confidence": 0,
            "error": "Invalid or empty product name"
        }

    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": name})
        response.raise_for_status()

        predictions = response.json()

        if not isinstance(predictions, list) or not predictions[0]:
            raise ValueError("Empty or unexpected API response")

        # Find the label with the highest confidence
        top_prediction = max(predictions[0], key=lambda x: x["score"])

        return {
            "label": top_prediction["label"].upper(),  # POSITIVE or NEGATIVE
            "confidence": round(top_prediction["score"] * 100, 2)
        }

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return {
            "label": "ERROR",
            "confidence": 0,
            "error": str(e)
        }

    except (KeyError, IndexError, ValueError) as e:
        print(f"[ERROR] Unexpected response: {response.text}")
        return {
            "label": "ERROR",
            "confidence": 0,
            "error": "Invalid API response format"
        }
