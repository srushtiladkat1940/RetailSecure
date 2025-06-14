def check_spelling(name):
    """Check for suspicious brand name misspellings."""
    suspicious_words = ["Samzung", "Nkie", "Abibas", "Samsang", "Samsug", "Glaxy", "Applle"]
    return any(word.lower() in name.lower() for word in suspicious_words)


def is_fake_discount(price, mrp):
    """Flag if discount is more than 70% off."""
    try:
        price = float(price)
        mrp = float(mrp)
        if mrp <= 0:
            return False
        return (mrp - price) / mrp > 0.7
    except (ValueError, TypeError):
        return False


def is_low_rated(rating):
    """Mark as low-rated if rating < 2.5"""
    try:
        return float(rating) < 2.5
    except (ValueError, TypeError):
        return False


def detect_issues(product_data):
    """Aggregate issue checks for a given product."""
    name = product_data.get("name", "")
    price = product_data.get("price", 0)
    mrp = product_data.get("mrp", 0)
    rating = product_data.get("rating", 5)
    trusted_domain = product_data.get("trusted_domain", False)

    return {
        "misspelling": check_spelling(name),
        "fake_discount": is_fake_discount(price, mrp),
        "low_ratings": is_low_rated(rating),
        "suspicious_domain": not trusted_domain
    }
