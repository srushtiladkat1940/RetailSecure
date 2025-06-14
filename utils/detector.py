def check_spelling(name):
    suspicious_words = ["Samzung", "Nkie", "Abibas"]
    return any(word.lower() in name.lower() for word in suspicious_words)

def is_fake_discount(price, mrp):
    if mrp <= 0:
        return False
    return (mrp - price) / mrp > 0.7  # More than 70% off is suspicious

def is_low_rated(rating):
    return rating < 2.5

def detect_issues(product_data):
    return {
        "misspelling": check_spelling(product_data["name"]),
        "fake_discount": is_fake_discount(product_data["price"], product_data["mrp"]),
        "low_ratings": is_low_rated(product_data.get("rating", 5)),
        "suspicious_domain": not product_data.get("trusted_domain", False)
    }
