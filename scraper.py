import asyncio
import csv
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from bs4 import BeautifulSoup

# Define directories and file paths
BASE_DIR = r"C:\Users\OMAR\.gemini\antigravity-ide\scratch\cars_scraper"
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")
CSV_PATH = os.path.join(BASE_DIR, "mercedes_benz_cars.csv")

# Create base directory if it doesn't exist
os.makedirs(BASE_DIR, exist_ok=True)

def parse_card(card):
    # Link
    link_el = card.select_one("a.vehicle-card-link") or card.select_one("a[href*='/vehicledetail']")
    link = ""
    if link_el and link_el.get("href"):
        href = link_el.get("href")
        link = href if href.startswith("http") else "https://www.cars.com" + href
    
    # Title
    title_el = card.select_one("h2.title") or card.select_one(".vehicle-card-title") or card.select_one(".title")
    title = title_el.text.strip() if title_el else "N/A"
    
    # Price
    price_el = card.select_one("span.primary-price") or card.select_one(".primary-price") or card.select_one(".price")
    price = price_el.text.strip() if price_el else "N/A"
    
    # Mileage
    mileage_el = card.select_one("div.mileage") or card.select_one(".mileage") or card.select_one(".mileage-number")
    mileage = mileage_el.text.strip() if mileage_el else "N/A"
    
    # Dealer Name
    dealer_el = card.select_one("div.dealer-name") or card.select_one(".dealer-name") or card.select_one(".seller-info")
    dealer_name = dealer_el.text.strip() if dealer_el else "N/A"
    
    # Dealer Rating
    rating_el = card.select_one("span.sds-rating__link") or card.select_one("span.dealer-rating") or card.select_one(".rating-number") or card.select_one(".sds-rating__number")
    dealer_rating = "N/A"
    if rating_el:
        dealer_rating = rating_el.text.strip()
    else:
        # Fallback to search inside card for something resembling rating
        for r_el in card.select(".sds-rating__number, .rating, .dealer-rating-number"):
            if r_el:
                dealer_rating = r_el.text.strip()
                break

    # Image
    img_el = card.select_one("img.vehicle-image") or card.select_one("img")
    image_url = ""
    if img_el:
        image_url = (
            img_el.get("src") or 
            img_el.get("data-src") or 
            img_el.get("data-lazy-src") or 
            img_el.get("srcset") or 
            ""
        )
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url
            
    return {
        "title": title,
        "price": price,
        "mileage": mileage,
        "dealer_name": dealer_name,
        "dealer_rating": dealer_rating,
        "link": link,
        "image_url": image_url
    }

async def scrape_page(page, page_num):
    url = f"https://www.cars.com/shopping/results/?makes[]=mercedes_benz&page={page_num}"
    print(f"Navigating to Page {page_num}: {url}")
    
    # Navigate
    await page.goto(url, timeout=60000)
    
    # Wait for the cards to load (allowing time for Turnstile challenge solving if needed)
    print("Waiting for vehicle cards to appear on the page...")
    try:
        await page.wait_for_selector("div.vehicle-card", timeout=60000)
        print(f"Page {page_num} loaded successfully!")
    except Exception as e:
        print(f"Timeout/Error waiting for vehicle cards on page {page_num}: {e}")
        # Take a debug screenshot
        screenshot_path = os.path.join(BASE_DIR, f"debug_page_{page_num}.png")
        await page.screenshot(path=screenshot_path)
        print(f"Saved debug screenshot to {screenshot_path}")
        return []

    # Let the lazy images load by scrolling slightly
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
    await page.wait_for_timeout(1000)
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(1000)

    # Get HTML content and parse with BeautifulSoup
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    cards = soup.select("div.vehicle-card")
    
    page_data = []
    for card in cards:
        parsed = parse_card(card)
        if parsed["title"] != "N/A":  # Avoid blank cards
            page_data.append(parsed)
            
    print(f"Extracted {len(page_data)} listings from Page {page_num}.")
    return page_data

async def main():
    all_data = []
    pages_to_scrape = 5  # Customize number of pages to scrape
    
    print("Launching Playwright browser with persistent context...")
    print("A Chrome browser window will open.")
    print("IMPORTANT: If a Cloudflare Turnstile 'Verify you are human' checkbox appears, please click it to verify!")
    
    async with async_playwright() as p:
        # Launch headful browser with persistent user data context
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            channel="chrome",
            viewport={"width": 1280, "height": 800}
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        for p_num in range(1, pages_to_scrape + 1):
            page_data = await scrape_page(page, p_num)
            if not page_data:
                print("No data extracted. Stopping scraper.")
                break
            all_data.extend(page_data)
            
            # Short delay between page requests
            await asyncio.sleep(2)
            
        await context.close()
        
    # Save to CSV
    if all_data:
        print(f"\nScraping complete. Saving {len(all_data)} listings to {CSV_PATH}...")
        keys = all_data[0].keys()
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(all_data)
        print("CSV saved successfully!")
    else:
        print("\nNo data collected to write to CSV.")

if __name__ == "__main__":
    asyncio.run(main())
