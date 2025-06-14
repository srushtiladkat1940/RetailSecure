import os
import requests
from flask import Flask, render_template, request
from urllib.parse import urlparse
from utils.detector import detect_issues
from utils.model import classify_name

app = Flask(__name__)

FAKESTORE_BASE = "https://fakestoreapi.com/products/"

def fetch_product_details(product_url):
    try:
        parsed = urlparse(product_url)
        product_id = parsed.path.strip("/").split("/")[-1]
        if not product_id.isdigit():
            return {"error": "Invalid product ID in URL."}

        response = requests.get(f"{FAKESTORE_BASE}{product_id}")
        if response.status_code != 200:
            return {"error": f"API returned status code {response.status_code}"}

        data = response.json()
        return {
            "name": data.get("title", "Unknown"),
            "price": data.get("price", 0),
            "mrp": round(data.get("price", 0) * 1.8, 2),  # Simulated MRP
            "rating": data.get("rating", {}).get("rate", 0),
            "product_id": data.get("id", "N/A"),
            "image": data.get("image", ""),
            "domain": urlparse(product_url).netloc,
            "trusted_domain": "fakestoreapi.com" in product_url
        }

    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product_url = request.form.get("product_url")
        product_data = fetch_product_details(product_url)

        if "error" in product_data:
            return render_template("index.html", product=product_data)

        issues = detect_issues(product_data)
        ai_result = classify_name(product_data["name"])
        return render_template("index.html", product=product_data, issues=issues, ai_result=ai_result)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
