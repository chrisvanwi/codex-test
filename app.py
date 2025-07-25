import os
from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Amazon Warehouse Deals</title>
</head>
<body>
    <h1>Amazon Warehouse Deals</h1>
    <ul>
    {% for deal in deals %}
        <li><a href='{{ deal.link }}' target='_blank'>{{ deal.title }}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
"""

AMAZON_URL = "https://www.amazon.de/s?i=warehouse-deals"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)

@app.route('/')
def index():
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        response = requests.get(AMAZON_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        deals = []
        for item in soup.select('div.s-result-item'):
            title_tag = item.select_one('h2 a span')
            link_tag = item.select_one('h2 a')
            if title_tag and link_tag:
                deals.append({
                    'title': title_tag.get_text(strip=True),
                    'link': 'https://www.amazon.de' + link_tag['href']
                })
            if len(deals) >= 10:
                break
    except Exception as e:
        deals = []
    return render_template_string(TEMPLATE, deals=deals)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
