import requests

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HEADERS = {"Authorization": "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"}  # Replace with your real token

def classify_name(name):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": name})
    result = response.json()[0][0]
    return {
        "label": result["label"],
        "confidence": round(result["score"] * 100, 2)
    }
