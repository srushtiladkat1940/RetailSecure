import os
from flask import Flask, render_template, request
from utils.walmart_api import fetch_product_details
from utils.detector import detect_issues
from utils.model import classify_name

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query1 = request.form.get("product1")

        # Fetch only the first product from Walmart API
        product1 = fetch_product_details(query1)

        if "error" in product1:
            return render_template("index.html", error=product1["error"])

        # Hardcoded fake product for product2
        product2 = {
            "name": "Samzung Galaxi S23 Ultraa",
            "price": 8999,
            "mrp": 79999,
            "rating": 1.2,
            "product_id": "fake-s23",
            "domain": "fake-deals.com",
            "trusted_domain": False,
            "image": "https://example.com/fake.jpg",
            "link": "https://fake-deals.com/s23"
        }

        issues1 = detect_issues(product1)
        issues2 = {
            "misspelling": True,
            "fake_discount": True,
            "low_ratings": True,
            "suspicious_domain": True
        }

        ai_result1 = classify_name(product1["name"])
        ai_result2 = {
            "label": "NEGATIVE",
            "confidence": 92.3
        }

        return render_template("index.html",
                               product1=product1, product2=product2,
                               issues1=issues1, issues2=issues2,
                               ai_result1=ai_result1, ai_result2=ai_result2)

    return render_template("index.html")
