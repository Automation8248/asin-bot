import os
import time
import requests
from playwright.sync_api import sync_playwright

# GitHub Secrets
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TARGET_COUNT = 10
asins = set()

print("Launching Playwright Browser with Proxy...")

def run_scraper():
    # Playwright start karna
    with sync_playwright() as p:
        # Asli Chromium browser launch karna (headless=True matlab background me chalega)
        browser = p.chromium.launch(
            headless=True,
            proxy={
                "server": "http://31.59.20.176:6754",
                "username": "oxulhyvs",
                "password": "ukzzq3m862fa"
            }
        )
        
        # Browser ka context set karna (Tier-1 USA ki feeling dene ke liye)
        context = browser.new_context(
            locale="en-US",
            timezone_id="America/New_York",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        for page_num in range(1, 10):
            if len(asins) >= TARGET_COUNT:
                break

            url = f"https://www.amazon.com/s?k=kitchen+gadgets&page={page_num}"
            print(f"Loading Page {page_num}...")
            
            try:
                # Page open karna
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # Human-like delay taaki page poora load ho jaye
                time.sleep(3)
                
                # Playwright se direct 'data-asin' nikalna (Regex ki zaroorat nahi)
                elements = page.locator("div[data-asin]").all()
                
                added_now = 0
                for el in elements:
                    asin = el.get_attribute("data-asin")
                    if asin and len(asin) == 10:
                        asins.add(asin)
                        added_now += 1
                        if len(asins) >= TARGET_COUNT:
                            break
                            
                print(f"Found {added_now} ASINs on Page {page_num}. Total: {len(asins)}/{TARGET_COUNT}")
                
            except Exception as e:
                print(f"Error on page {page_num}: {e}")

        browser.close()

# Scraper function chalana
run_scraper()

# --- Telegram Messaging Logic ---
asin_list = list(asins)[:TARGET_COUNT]

if asin_list:
    print(f"\nSending {len(asin_list)} ASINs to Telegram...")
    
    # Sequence mein plain text message
    message = "🇺🇸 Tier-1 Kitchen Products (Playwright):\n\n"
    for index, asin in enumerate(asin_list, start=1):
        message += f"{index}. {asin}\n"

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
    print("✅ Successfully Sent to Telegram!")
else:
    print("⚠️ 0 ASINs found. Proxy ya Amazon ne block kiya hoga.")
