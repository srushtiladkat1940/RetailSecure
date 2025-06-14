import os
from flask import Flask, render_template, request
from utils.walmart_api import fetch_product_details
from utils.detector import detect_issues
from utils.model import classify_name

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product_url = request.form.get("product_url")
        product_data = fetch_product_details(product_url)
        issues = detect_issues(product_data)
        ai_result = classify_name(product_data["name"])
        return render_template("index.html", product=product_data, issues=issues, ai_result=ai_result)
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
