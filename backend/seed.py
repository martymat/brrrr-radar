from decimal import Decimal
from db import SessionLocal
from models import Property, PropertyPhoto

PROPERTIES = [
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/1001",
        "address": "123 Main St",
        "city": "Staten Island",
        "state": "NY",
        "zip": "10301",
        "price": Decimal("525000"),
        "beds": 3,
        "baths": Decimal("2.0"),
        "sqft": 1450,
        "description": "Solid brick home near ferry. Needs light rehab.",
        "photos": 3,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/1002",
        "address": "45 Bay St",
        "city": "Staten Island",
        "state": "NY",
        "zip": "10301",
        "price": Decimal("610000"),
        "beds": 4,
        "baths": Decimal("2.5"),
        "sqft": 1800,
        "description": "Large single-family with basement unit.",
        "photos": 4,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/1003",
        "address": "789 Forest Ave",
        "city": "Staten Island",
        "state": "NY",
        "zip": "10310",
        "price": Decimal("475000"),
        "beds": 2,
        "baths": Decimal("1.0"),
        "sqft": 1100,
        "description": "Fixer-upper with strong rental upside.",
        "photos": 2,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/2001",
        "address": "12 Maple St",
        "city": "Newark",
        "state": "NJ",
        "zip": "07102",
        "price": Decimal("390000"),
        "beds": 3,
        "baths": Decimal("1.5"),
        "sqft": 1350,
        "description": "Cash-flow oriented BRRR candidate.",
        "photos": 3,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/2002",
        "address": "88 Market St",
        "city": "Newark",
        "state": "NJ",
        "zip": "07105",
        "price": Decimal("425000"),
        "beds": 4,
        "baths": Decimal("2.0"),
        "sqft": 1600,
        "description": "Two-unit property with separate entrances.",
        "photos": 4,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/3001",
        "address": "301 Oak Dr",
        "city": "Scranton",
        "state": "PA",
        "zip": "18503",
        "price": Decimal("265000"),
        "beds": 3,
        "baths": Decimal("1.0"),
        "sqft": 1200,
        "description": "Low purchase price, strong rent ratios.",
        "photos": 2,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/3002",
        "address": "77 Pine St",
        "city": "Scranton",
        "state": "PA",
        "zip": "18504",
        "price": Decimal("295000"),
        "beds": 4,
        "baths": Decimal("2.0"),
        "sqft": 1550,
        "description": "Value-add opportunity near downtown.",
        "photos": 3,
    },
    {
        "listing_source": "manual",
        "listing_url": "https://example.com/listing/4001",
        "address": "9 Cedar Ln",
        "city": "Buffalo",
        "state": "NY",
        "zip": "14201",
        "price": Decimal("215000"),
        "beds": 3,
        "baths": Decimal("1.0"),
        "sqft": 1150,
        "description": "Classic BRRR market with strong rents.",
        "photos": 2,
    },
]

def seed():
    session = SessionLocal()
    try:
        print("Seeding properties...")

        for idx, data in enumerate(PROPERTIES, start=1):
            photos_count = data.pop("photos")

            prop = Property(**data)
            session.add(prop)
            session.flush()  # assigns prop.id

            for i in range(1, photos_count + 1):
                session.add(
                    PropertyPhoto(
                        property_id=prop.id,
                        photo_url=f"https://picsum.photos/seed/brrrr-{prop.id}-{i}/800/600",
                        sort_order=i,
                    )
                )

            print(f"  ✔ Inserted property id={prop.id}")

        session.commit()
        print("Done seeding.")
    finally:
        session.close()

if __name__ == "__main__":
    seed()
