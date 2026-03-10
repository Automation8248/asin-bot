import requests
import re
import time

BOT_TOKEN = "8797653971:AAGeiZQVtOLGn4gU3g3WRnYCgLRMWShVwLg"
CHAT_ID = "7584043609"

headers = {
    "User-Agent": "Mozilla/5.0"
}

asins = set()

for page in range(1, 21):
    url = f"https://www.amazon.com/s?k=kitchen+gadgets&page={page}"
    r = requests.get(url, headers=headers)
    
    found = re.findall(r'/dp/([A-Z0-9]{10})', r.text)
    
    for a in found:
        asins.add(a)

    time.sleep(2)

for asin in asins:

    link = f"https://www.amazon.com/dp/{asin}"

    message = f"""
Kitchen Product Found 🍳

ASIN: {asin}

Link:
{link}
"""

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
