# Codex Test Repository

This is a test repository initialized for use with Codex.

## Amazon Warehouse Deals Website

This repository now includes a small Flask application that fetches and displays
Amazon Warehouse deals. The application attempts to scrape the public Warehouse
Deals search page from Amazon Germany and shows up to the first ten results.

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000` to see the deals.

Note that Amazon may restrict automated requests. If no deals are displayed,
the request may have been blocked by Amazon or additional headers may be
required.
