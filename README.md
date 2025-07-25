# Codex Test Repository

This is a test repository initialized for use with Codex.

## Amazon Warehouse Deals Website

This repository now includes a small Flask application that fetches and displays
Amazon Warehouse deals. The application attempts to scrape the public Warehouse
Deals search page from Amazon Germany. You can search for specific products and
limit the number of displayed results with an environment variable.

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application (optional: set `MAX_DEALS` to limit results):
   ```bash
   MAX_DEALS=5 python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000` to search and view the deals.

Note that Amazon may restrict automated requests. If no deals are displayed,
the request may have been blocked by Amazon or additional headers may be
required.
