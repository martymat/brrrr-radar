Goal: “Scrape listings → store → score → browse UI”

MVP screens:
- Property List (filters + score)
- Property Detail (photos + analysis)
- Run Scrape (trigger job + show results)

MVP data fields
- listing_source (string)
- listing_url (unique)
- address/city/state/zip
- price (int), beds (numeric), baths (numeric), sqft (int)
- description (text nullable)
- photo_urls (list)
- scraped_at (datetime)
- analysis: score_total (0–100), breakdown, reasons

Scores
- Subscores (0–25 each): Value, Size, Risk, Liquidity
- score_total = sum(subscores)
- reasons = array of 3–5 strings (“Under market $/sqft”, “Good bed/bath ratio”, etc.)
