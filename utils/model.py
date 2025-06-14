import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

def classify_name(name):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": name})
    
    if response.status_code != 200:
        return {
            "label": "ERROR",
            "confidence": 0,
            "error": response.json().get("error", "Unknown error")
        }

    result = response.json()[0][0]
    return {
        "label": result["label"],
        "confidence": round(result["score"] * 100, 2)
    }
