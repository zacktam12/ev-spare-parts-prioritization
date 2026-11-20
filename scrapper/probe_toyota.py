"""Deep probe of Toyota spare parts site for bZ4X parts structure."""
import httpx, sys, time
sys.path.insert(0, ".")
from bs4 import BeautifulSoup
from config import config

client = httpx.Client(headers=config.random_headers, timeout=15.0, follow_redirects=True)

# 1. Get bZ4X 2023 page (most common year in Ethiopian market)
print("=== Toyota bZ4X 2023 - Category Links ===")
html = client.get("https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023").text
soup = BeautifulSoup(html, "html.parser")

# Find category/group links
all_links = soup.find_all("a", href=True)
category_links = []
for a in all_links:
    href = a.get("href", "")
    text = a.get_text(strip=True)
    if "/BZ4X/2023/" in href and text:
        category_links.append((text, href))
        print(f"  {text[:60]:<60} -> {href}")

print(f"\nTotal category links found: {len(category_links)}")

# 2. Check a specific category for part structure
# Look for brake-related, lighting, body links
target_keywords = ["brake", "light", "lamp", "bumper", "mirror", "fender", "wiper", "filter", "shock", "absorber", "body"]
relevant = [(t, h) for t, h in category_links if any(k in t.lower() for k in target_keywords)]
print(f"\nRelevant categories for our 10 part types: {len(relevant)}")
for text, href in relevant:
    print(f"  {text}")

# 3. Dive into first relevant category to see part listing structure
if relevant:
    test_text, test_href = relevant[0]
    full_url = f"https://www.toyota-spare-parts.com{test_href}" if test_href.startswith("/") else test_href
    print(f"\n=== Diving into: {test_text} -> {full_url} ===")
    time.sleep(1)
    html2 = client.get(full_url).text
    soup2 = BeautifulSoup(html2, "html.parser")
    
    # Look for part listings
    # Try common patterns
    for selector in [".part-row", ".product-item", "tr", ".part-number", ".item-row", ".parts-list li", "table tr"]:
        items = soup2.select(selector)
        if items and len(items) > 2:
            print(f"\n  Found {len(items)} elements with '{selector}'")
            for item in items[:5]:
                print(f"    {item.get_text(strip=True)[:120]}")
            break

client.close()
print("\nDone.")
