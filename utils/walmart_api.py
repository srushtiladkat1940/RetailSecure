import requests
from urllib.parse import urlparse, parse_qs

TRUSTED_DOMAINS = [
    "www.walmart.com",
    "www.flipkart.com",
    "www.amazon.in",
    "www.amazon.com"
]

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_trusted_domain(domain):
    return domain.lower() in TRUSTED_DOMAINS

def fetch_product_details(product_url):
    parsed = urlparse(product_url)
    domain = parsed.netloc
    trusted = is_trusted_domain(domain)

    if "fakestoreapi.com" in domain:
        try:
            # extract product ID from the URL path like /products/1
            product_id = parsed.path.strip("/").split("/")[-1]
            response = requests.get(f"https://fakestoreapi.com/products/{product_id}")
            response.raise_for_status()
            data = response.json()

            return {
                "name": data.get("title", "Unknown"),
                "price": data.get("price", "N/A"),
                "mrp": round(data.get("price", 0) * 1.8, 2),  # fake inflated MRP
                "rating": data.get("rating", {}).get("rate", 0),
                "product_id": product_id,
                "domain": domain,
                "trusted_domain": trusted,
                "image": data.get("image", "")
            }
        except Exception as e:
            return {
                "name": "Error fetching data",
                "price": "N/A",
                "mrp": "N/A",
                "rating": 0,
                "product_id": "N/A",
                "domain": domain,
                "trusted_domain": trusted,
                "error": str(e)
            }

    # Default simulation for trusted domains like Amazon/Walmart
    product_id = parse_qs(parsed.query).get('id', ['123456'])[0]

    return {
        "name": "Samsung Smart TV 55inch",
        "price": 299.99,
        "mrp": 999.99,
        "rating": 2.0,
        "product_id": product_id,
        "domain": domain,
        "trusted_domain": trusted
    }
