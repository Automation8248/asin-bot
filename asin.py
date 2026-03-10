import os
import requests
import re
import time

# GitHub Secrets se token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Aapka original header + USA Tier-1 location batane ke liye language
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

asins = set()

print("Scraping started...")

# Aapka original loop
for page in range(1, 21):
    # Aapki requirement ke hisaab se max 60 ASINs
    if len(asins) >= 60:
        break

    url = f"https://www.amazon.com/s?k=kitchen+gadgets&page={page}"
    r = requests.get(url, headers=headers)
    print(f"Page {page} Status: {r.status_code}")
    
    # Aapka original Regex Logic
    found = re.findall(r'/dp/([A-Z0-9]{10})', r.text)
    
    for a in found:
        asins.add(a)
        if len(asins) >= 60: # 60 hote hi ruk jaye
            break

    # Aapka original sleep
    time.sleep(2)

print(f"Total ASINs found: {len(asins)}")

# Aapka original Telegram message bhejne ka logic (Ek-ek karke message aayega)
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
    
    # Telegram ek second me max 30 message allow karta hai, isliye 1 sec ka delay zaroori hai
    time.sleep(1) 

print("Done!")
