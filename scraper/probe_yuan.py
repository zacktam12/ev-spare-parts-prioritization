"""Quick probe: find Yuan Up parts on Landin and check available BYD model pages."""
import httpx, json, sys
sys.path.insert(0, ".")
from bs4 import BeautifulSoup
from config import config

client = httpx.Client(headers=config.random_headers, timeout=15.0, follow_redirects=True)

# 1. Try direct Yuan Up URLs
print("=== Checking direct Yuan Up URLs ===")
for url in [
    "https://www.landinparts.com/byd-yuan-up/",
    "https://www.landinparts.com/byd/yuan-up/",
    "https://www.landinparts.com/byd-yuan/",
    "https://www.landinparts.com/yuan-up/",
]:
    try:
        resp = client.get(url)
        print(f"  {resp.status_code} - {url}")
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select(".product-card-wrap")
            print(f"       -> {len(cards)} product cards")
    except Exception as e:
        print(f"  ERROR - {url}: {e}")

# 2. Check main Landin homepage for BYD-related nav
print("\n=== BYD links on Landin homepage ===")
html = client.get("https://www.landinparts.com/").text
soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a", href=True)
for a in links:
    href = a.get("href", "")
    text = a.get_text(strip=True)
    if "byd" in href.lower() or "byd" in text.lower():
        print(f"  {text[:60]:<60} -> {href}")

# 3. Check if the /byd/ page has model filter tabs/buttons
print("\n=== Model filter elements on /byd/ page ===")
html = client.get("https://www.landinparts.com/byd/").text
soup = BeautifulSoup(html, "html.parser")
# Look for filter/tab/dropdown elements
for selector in [".model-filter", ".filter-bar", ".tab-item", ".brand-models", "[data-model]", ".model-nav"]:
    elems = soup.select(selector)
    if elems:
        print(f"  Found {len(elems)} elements matching '{selector}'")
        for e in elems[:5]:
            print(f"    {e.get_text(strip=True)[:80]}")

# Check for JS data with model listings
scripts = soup.find_all("script")
for s in scripts:
    text = s.string or ""
    if "yuan" in text.lower():
        print(f"\n  Found 'yuan' mention in script tag (first 200 chars):")
        idx = text.lower().index("yuan")
        print(f"    ...{text[max(0,idx-80):idx+120]}...")

client.close()
print("\nDone.")
