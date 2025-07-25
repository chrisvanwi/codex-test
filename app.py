import os
from functools import lru_cache
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

AMAZON_URL = "https://www.amazon.de/s?i=warehouse-deals"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)

MAX_DEALS = int(os.environ.get("MAX_DEALS", "10"))


@lru_cache(maxsize=32)
def fetch_deals(query: str):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = AMAZON_URL
    if query:
        url += "&k=" + quote_plus(query)
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    deals = []
    for item in soup.select('div.s-result-item'):
        title_tag = item.select_one('h2 a span')
        link_tag = item.select_one('h2 a')
        price_tag = item.select_one('span.a-price span.a-offscreen')
        if title_tag and link_tag:
            deal = {
                'title': title_tag.get_text(strip=True),
                'link': 'https://www.amazon.de' + link_tag['href']
            }
            if price_tag:
                deal['price'] = price_tag.get_text(strip=True)
            deals.append(deal)
        if len(deals) >= MAX_DEALS:
            break
    return deals


@app.route('/')
def index():
    query = request.args.get('q', '')
    error = None
    deals = []
    try:
        deals = fetch_deals(query)
    except Exception as exc:
        error = str(exc)
    return render_template('index.html', deals=deals, query=query, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
