from flask import Flask, jsonify
from scraper.zillow_scraper import scrape_properties

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def trigger_scrape():
    listings = scrape_properties()
    return jsonify({"message": "Scrape complete", "count": len(listings)})