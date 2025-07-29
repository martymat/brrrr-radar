import requests
from bs4 import BeautifulSoup

def scrape_properties():
    url = "https://www.realtor.com/realestateandhomes-search/New-York_NY"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = []

    for card in soup.select(".component_property-card"):
        try:
            address = card.select_one(".address").text
            price = card.select_one(".price").text
            beds = card.select_one(".property-beds").text if card.select_one(".property-beds") else "N/A"
            listings.append({
                "address": address.strip(),
                "price": price.strip(),
                "beds": beds.strip()
            })
        except:
            continue

    return listings