from transformers import pipeline

# You can replace this with a fine-tuned model path later
classifier = pipeline("text-classification", model="bert-base-uncased")

def classify_name(name):
    result = classifier(name)[0]
    return {
        "label": result["label"],
        "confidence": round(result["score"] * 100, 2)
    }
