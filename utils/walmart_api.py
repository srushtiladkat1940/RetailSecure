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
    query_params = parse_qs(parsed.query)
    product_id = query_params.get('id', ['123456'])[0]

    domain = parsed.netloc

    # Simulated API response
    return {
        "name": "Samsung Smart TV 55inch",
        "price": 299.99,
        "mrp": 999.99,
        "rating": 2.0,
        "product_id": product_id,
        "domain": domain,
        "trusted_domain": is_trusted_domain(domain)
    }
