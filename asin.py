import os
import time
import random
import requests
from playwright.sync_api import sync_playwright

# GitHub Secrets se token fetch karna
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Aapki di hui Kitchen Products ki list
kitchen_products = [
    # 1–40: Popular Appliances
    "Air fryer", "Air fryer toaster oven", "Pressure cooker", "Multi-cooker", 
    "Rice cooker", "Slow cooker", "Countertop blender", "Personal smoothie blender", 
    "Food processor", "Stand mixer", "Hand mixer", "Electric kettle", 
    "Espresso machine", "Coffee maker", "Coffee grinder", "Milk frother", 
    "Toaster", "Toaster oven", "Electric griddle", "Electric skillet", 
    "Panini press", "Electric grill", "Electric egg cooker", "Ice cream maker", 
    "Bread maker", "Sous vide cooker", "Electric meat grinder", "Electric pasta maker", 
    "Electric juicer", "Cold press juicer", "Ice maker machine", "Electric tortilla maker", 
    "Electric waffle maker", "Electric popcorn maker", "Electric hot pot", 
    "Electric steamer", "Countertop pizza oven", "Smart WiFi cooker", 
    "Smart oven", "Smart air fryer",

    # 41–80: Viral Kitchen Gadgets
    "Vegetable chopper", "Mandoline slicer", "Spiralizer", "Garlic press", 
    "Lemon squeezer", "Avocado slicer", "Apple slicer", "Egg slicer", 
    "Cherry pitter", "Pineapple corer", "Herb scissors", "Kitchen scissors", 
    "Rotary cheese grater", "Microplane zester", "Potato masher", "Meat tenderizer", 
    "Burger press", "Dumpling maker", "Tortilla press", "Sushi rolling kit", 
    "Corn stripper", "Onion holder slicer", "Butter slicer", "Pizza cutter", 
    "Bench scraper", "Dough scraper", "Salad chopper bowl", "Salad spinner", 
    "Oil sprayer bottle", "Basting brush", "Meat injector", "Digital food thermometer", 
    "Candy thermometer", "Magnetic knife holder", "Knife sharpening stone", 
    "Kitchen scale", "Food cutting board set", "Rolling chopper", "Vegetable dicer", 
    "Meat shredder claws",

    # 81–120: Baking Products
    "Baking sheet", "Silicone baking mat", "Cake pan", "Springform pan", 
    "Muffin pan", "Cupcake pan", "Bundt pan", "Bread loaf pan", "Donut pan", 
    "Tart pan", "Pie dish", "Brownie pan", "Pizza stone", "Pizza peel", 
    "Rolling pin", "Cookie cutters", "Cookie scoop", "Cookie press", 
    "Cooling rack", "Cake decorating kit", "Piping bags", "Icing spatula", 
    "Cake turntable", "Cake leveler", "Cake scraper", "Fondant smoother", 
    "Pastry brush", "Pastry blender", "Dough whisk", "Bread proofing basket", 
    "Bread lame scoring tool", "Oven thermometer", "Pastry mat", "Cake stand", 
    "Cupcake carrier", "Cake carrier", "Dough divider", "Pie weights", 
    "Biscuit cutter", "Chocolate mold",

    # 121–150: Kitchen Storage
    "Airtight food containers", "Glass meal prep containers", "Vacuum food sealer", 
    "Vacuum sealer bags", "Bread box", "Produce storage container", 
    "Fridge organizer bins", "Refrigerator egg holder", "Soda can organizer", 
    "Spice rack", "Magnetic spice jars", "Drawer organizers", "Dish drying rack", 
    "Sink caddy", "Under-sink organizer", "Pantry shelf organizer", 
    "Lazy Susan turntable", "Cabinet shelf riser", "Pot lid organizer", 
    "Hanging pot rack", "Mug tree", "Coffee pod holder", "Tea bag organizer", 
    "Oil dispenser bottle", "Honey dispenser", "Flour storage container", 
    "Rice storage container", "Lunch box", "Bento box", "Insulated food jar",

    # 151–183: Smart & Cleaning Kitchen Tools
    "Motion sensor trash can", "Compost bin", "Automatic soap dispenser", 
    "Sink strainer", "Sink stopper", "Bottle cleaning brush", "Straw cleaning brush", 
    "Drain cleaner tool", "Garbage disposal cleaner", "Kitchen mop", 
    "Countertop cleaning wipes", "Oven cleaner", "Microwave cleaner", 
    "Fridge cleaner", "Dishwasher cleaner", "Steam cleaner", "Smart kitchen scale", 
    "Bluetooth meat thermometer", "Smart fridge camera", "Smart kitchen display", 
    "Smart coffee maker", "Smart kettle", "Smart oven", "Voice-controlled microwave", 
    "Automatic pan stirrer", "Digital timer", "Magnetic timer", "Recipe stand", 
    "Tablet holder for kitchen", "Cookbook stand", "Grocery list board", 
    "Magnetic whiteboard planner", "Electric jar opener"
]

TARGET_COUNT = 10

def run_scraper():
    # Randomly ek product select karna
    selected_product = random.choice(kitchen_products)
    search_query = selected_product.replace(" ", "+")
    print(f"Today's Selected Product: {selected_product}")
    
    asins = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={
                "server": "http://31.59.20.176:6754",
                "username": "oxulhyvs",
                "password": "ukzzq3m862fa"
            }
        )
        
        context = browser.new_context(
            locale="en-US",
            timezone_id="America/New_York",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        # 10 ASINs pehle page par hi mil jayenge, isliye zyada pages scan karne ki zaroorat nahi
        url = f"https://www.amazon.com/s?k={search_query}&page=1"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3) # Human-like delay
            
            elements = page.locator("div[data-asin]").all()
            
            for el in elements:
                asin = el.get_attribute("data-asin")
                
                # NAYA LOGIC: Check karega ki product ka naam page ke text mein hai ya nahi
                try:
                    card_text = el.inner_text().lower()
                    is_kitchen_related = selected_product.lower() in card_text
                except:
                    is_kitchen_related = False

                # Check valid 10-character ASIN aur strictly kitchen match
                if asin and len(asin) == 10 and asin.isupper() and is_kitchen_related:
                    asins.add(asin)
                    if len(asins) >= TARGET_COUNT:
                        break
                        
        except Exception as e:
            print(f"Error while scraping: {e}")

        browser.close()
        
    return list(asins)[:TARGET_COUNT]

# Script run karna
final_asins = run_scraper()

# Telegram Messaging
if final_asins:
    # ⚠️ SIRF ASIN numbers, koi extra text nahi jaisa aapne manga tha
    message = "\n".join(final_asins)

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
    print(f"✅ Sent {len(final_asins)} pure ASINs to Telegram!")
else:
    print("⚠️ 0 ASINs found. Proxy ya block ka issue ho sakta hai.")
