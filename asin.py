import os
import requests
import re
import time
import random

# GitHub Secrets se token fetch karna
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 50+ Real Browser User-Agents (To bypass 503)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    # (Aap isme aur UAs daal sakte hain)
]

# Random Tier-1 Kitchen keywords
keywords = ["kitchen gadgets", "kitchen accessories", "smart kitchen tools", "baking supplies"]
selected_keyword = random.choice(keywords).replace(" ", "+")

asins = set()
TARGET_COUNT = 60

print(f"Targeting {TARGET_COUNT} ASINs for Tier-1 (USA) market...")
print(f"Keyword: {selected_keyword.replace('+', ' ')}")

# Requests Session use kar rahe hain taaki cookies store hon aur human lage
session = requests.Session()

for page in range(1, 10):
    if len(asins) >= TARGET_COUNT:
        break

    url = f"https://www.amazon.com/s?k={selected_keyword}&page={page}"
    
    # 503 Bypass karne ke liye extremely strict headers
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }

    print(f"Fetching Page {page}...")
    try:
        r = session.get(url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            # Regex se ASIN nikalna (Aapke original logic ke hisaab se)
            found_url = re.findall(r'/dp/([A-Z0-9]{10})', r.text)
            found_data = re.findall(r'data-asin="([A-Z0-9]{10})"', r.text)
            
            # Dono regex results ko combine karna
            all_found = set(found_url + found_data)
            
            added_now = 0
            for a in all_found:
                if len(a) == 10 and a.isupper(): # ASIN hamesha 10 character ka capital hota hai
                    asins.add(a)
                    added_now += 1
                    if len(asins) >= TARGET_COUNT:
                        break
            
            print(f"  -> Found {added_now} ASINs. Total: {len(asins)}/{TARGET_COUNT}")
        else:
            print(f"  -> ❌ Amazon blocked request! Status Code: {r.status_code}")
            
    except Exception as e:
        print(f"  -> ❌ Request failed: {e}")

    # Random sleep is VERY important to avoid 503
    time.sleep(random.uniform(3.5, 7.5))

final_asins = list(asins)[:TARGET_COUNT]

# Telegram par bhejna (Aapka original 1-by-1 style spam ho jayega isliye isko text me list karke bhej rahe hain)
if final_asins:
    print(f"\nSending {len(final_asins)} ASINs to Telegram...")
    
    # Message format
    message = f"🇺🇸 Kitchen Products Found ({len(final_asins)} ASINs)\nKeyword: {selected_keyword.replace('+', ' ')}\n\n"
    for asin in final_asins:
        message += f"• {asin} (https://www.amazon.com/dp/{asin})\n"

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True # Telegram links ka preview na banaye taaki message clean rahe
        }
    )
    print("✅ Successfully Sent!")
else:
    print("⚠️ 503 Error still coming. GitHub IPs are completely blacklisted by Amazon.")
