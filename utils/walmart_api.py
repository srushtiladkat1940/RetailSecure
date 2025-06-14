import requests
import re

SERP_API_KEY = "f6e96ff0531de455248fd3a76534ce7e96f26f5ffbadb5f4bc2d88381788f3ce"  # Replace with your actual key

def parse_price(price_str):
    try:
        clean = re.sub(r'[^\d.]', '', price_str)
        return float(clean) if clean else 0.0
    except:
        return 0.0

def fetch_product_details(product_query):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": product_query,
        "api_key": SERP_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("shopping_results", [])

        if not results:
            return {"error": "No results found for this product."}

        product = results[0]
        price = parse_price(product.get("price", "₹0"))

        return {
            "name": product.get("title", "Unknown Product"),
            "price": price,
            "mrp": round(price * 1.8, 2) if price else 0.0,
            "rating": product.get("rating", 0),
            "product_id": product.get("product_id", "N/A"),
            "domain": "google.com",
            "trusted_domain": True,
            "image": product.get("thumbnail", ""),
            "link": product.get("link", "#")
        }

    except Exception as e:
        return {
            "name": "Error fetching product",
            "price": "N/A",
            "mrp": "N/A",
            "rating": 0,
            "product_id": "N/A",
            "domain": "unknown",
            "trusted_domain": False,
            "error": str(e)
        }
