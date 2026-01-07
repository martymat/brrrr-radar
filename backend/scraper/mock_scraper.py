from decimal import Decimal
import hashlib

def run_mock_scrape(query: str, max_results: int):
    items = []
    for i in range(max_results):
        h = hashlib.md5(f"{query}:{i}".encode("utf-8")).hexdigest()[:8]
        city = "Staten Island" if "staten" in query.lower() else "Newark"
        state = "NY" if city == "Staten Island" else "NJ"
        zip_code = "10301" if city == "Staten Island" else "07102"

        price = Decimal(str(250000 + (i * 25000)))
        beds = 2 + (i % 4)

        items.append({
            "listing_source": "mock",
            "listing_url": f"https://example.com/{h}",
            "address": f"{100 + i} {query.title()} St",
            "city": city,
            "state": state,
            "zip": zip_code,
            "price": price,
            "beds": beds,
            "baths": Decimal("1.0") if beds <= 2 else Decimal("2.0"),
            "sqft": 900 + (i * 120),
            "description": f"Mock listing for query='{query}'",
        })
    return items
