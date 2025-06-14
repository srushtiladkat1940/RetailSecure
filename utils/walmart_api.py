import requests

SERP_API_KEY = "f6e96ff0531de455248fd3a76534ce7e96f26f5ffbadb5f4bc2d88381788f3ce"  # Replace with your actual key

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

        # Use the first product found
        product = results[0]
        price_str = product.get("price", "₹0").replace("₹", "").replace(",", "")
        price = float(price_str) if price_str.replace('.', '', 1).isdigit() else 0.0

        return {
            "name": product.get("title", "Unknown Product"),
            "price": price,
            "mrp": round(price * 1.8, 2),  # inflated MRP for testing
            "rating": product.get("rating", 0),
            "product_id": product.get("product_id", "N/A"),
            "domain": "google.com",
            "trusted_domain": True,
            "image": product.get("thumbnail", ""),
            "link": product.get("link", "")
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
