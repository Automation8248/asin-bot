import os
import requests
import re
import time

# GitHub Secrets se token fetch karna
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Aapki Webshare Proxy
proxies = {
    "http": "http://oxulhyvs:ukzzq3m862fa@31.59.20.176:6754/",
    "https": "http://oxulhyvs:ukzzq3m862fa@31.59.20.176:6754/"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

asins = set()
print("Scraping started with Webshare Proxy...")

for page in range(1, 21):
    if len(asins) >= 60:
        break

    url = f"https://www.amazon.com/s?k=kitchen+gadgets&page={page}"
    
    try:
        # Proxy yahan requests.get mein add ki gayi hai
        r = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        print(f"Page {page} Status: {r.status_code}")
        
        # Aapka pasandida Regex logic
        found = re.findall(r'/dp/([A-Z0-9]{10})', r.text)
        
        for a in found:
            asins.add(a)
            if len(asins) >= 60:
                break
                
    except Exception as e:
        print(f"Error on Page {page}: {e}")

    time.sleep(2)

# Set ko list mein convert karke sequence banana
asin_list = list(asins)[:60]
print(f"Total ASINs found: {len(asin_list)}")

if asin_list:
    # Telegram message ko sequence (1, 2, 3...) mein banana
    message = "🍳 Tier-1 Kitchen Products:\n\n"
    
    for index, asin in enumerate(asin_list, start=1):
        message += f"{index}. {asin}\n"

    # Telegram par send karna
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
    print("✅ Message successfully sent to Telegram in sequence!")
else:
    print("⚠️ 503 Error. Agar abhi bhi error aa raha hai, toh Amazon ne is Proxy IP ko bhi block kar diya hai.")
