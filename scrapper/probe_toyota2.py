"""Dive into Toyota bZ4X catalogue to find part group structure."""
import httpx, sys, time
sys.path.insert(0, ".")
from bs4 import BeautifulSoup
from config import config

client = httpx.Client(headers=config.random_headers, timeout=15.0, follow_redirects=True)

# Pick one chassis variant and dive in
url = "https://www.toyota-spare-parts.com/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210"
print(f"=== Fetching chassis page: {url} ===")
time.sleep(1)
html = client.get(url).text
soup = BeautifulSoup(html, "html.parser")

# Find all links on this page
all_links = soup.find_all("a", href=True)
print(f"Total links: {len(all_links)}")

# Filter for part group/category links
category_links = []
for a in all_links:
    href = a.get("href", "")
    text = a.get_text(strip=True)
    if "561210" in href and text and len(text) > 2:
        category_links.append((text, href))

print(f"\nPart group links: {len(category_links)}")
for text, href in category_links[:40]:
    print(f"  {text[:70]}")

# Also check for any structured data or tables
tables = soup.find_all("table")
print(f"\nTables found: {len(tables)}")

# Check for target part categories
target_keywords = ["brake", "light", "lamp", "bumper", "mirror", "fender", "wiper", "filter", "shock", "absorber", "body", "panel"]
print(f"\nLinks matching our 10 categories:")
for text, href in category_links:
    tl = text.lower()
    matches = [k for k in target_keywords if k in tl]
    if matches:
        print(f"  [{', '.join(matches)}] {text[:70]} -> ...{href[-40:]}")

client.close()
print("\nDone.")
