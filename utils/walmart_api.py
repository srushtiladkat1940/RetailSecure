import requests
from urllib.parse import urlparse

def fetch_product_details(product_url):
    parsed_url = urlparse(product_url)
    domain = parsed_url.netloc.lower()
    
    # Only allow fakestoreapi for now
    if "fakestoreapi.com" in domain:
        try:
            product_id = parsed_url.path.strip("/").split("/")[-1]
            api_url = f"https://fakestoreapi.com/products/{product_id}"
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            return {
                "name": data.get("title"),
                "price": data.get("price"),
                "mrp": round(data.get("price", 0) * 1.5, 2),  # Fake MRP logic
                "rating": data.get("rating", {}).get("rate", 0),
                "product_id": product_id,
                "image": data.get("image"),
                "domain": domain,
                "trusted_domain": True
            }
        except Exception as e:
            return {"error": f"Failed to fetch product: {str(e)}"}
    
    return {"error": "Unsupported domain. Use fakestoreapi.com only for now."}
