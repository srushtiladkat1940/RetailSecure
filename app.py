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
        query2 = request.form.get("product2")

        # Fetch data from Google Shopping API
        product1 = fetch_product_details(query1)
        product2 = fetch_product_details(query2)

        if "error" in product1 or "error" in product2:
            error_msg = product1.get("error") or product2.get("error")
            return render_template("index.html", error=error_msg)

        # Inject original user query for spelling check
        product1["user_input"] = query1
        product2["user_input"] = query2

        issues1 = detect_issues(product1)
        issues2 = detect_issues(product2)

        ai_result1 = classify_name(product1["name"])
        ai_result2 = classify_name(product2["name"])

        return render_template("index.html",
                               product1=product1, product2=product2,
                               issues1=issues1, issues2=issues2,
                               ai_result1=ai_result1, ai_result2=ai_result2)

    return render_template("index.html")
