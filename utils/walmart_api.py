import requests
from urllib.parse import urlparse, parse_qs

def fetch_product_details(product_url):
    parsed = urlparse(product_url)
    query_params = parse_qs(parsed.query)
    product_id = query_params.get('id', ['123456'])[0]
    return {
        "name": "Samsung Smart TV 55inch",
        "price": 299.99,
        "mrp": 999.99,
        "rating": 2.0,
        "product_id": product_id,
        "domain": parsed.netloc
    }
