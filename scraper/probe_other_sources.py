"""Probe CQSW Auto Parts for Yuan Up / other BYD models, and check Toyota parts site."""
import httpx, sys
sys.path.insert(0, ".")
from bs4 import BeautifulSoup
from config import config

client = httpx.Client(headers=config.random_headers, timeout=15.0, follow_redirects=True)

# 1. CQSW - Check for Yuan Up pages
print("=== CQSW Auto Parts - BYD Models ===")
for url in [
    "https://www.cqswautoparts.com/part-numbers-for-byd-yuan-up-spare-parts",
    "https://www.cqswautoparts.com/part-numbers-for-byd-yuan-spare-parts",
    "https://www.cqswautoparts.com/byd-yuan-up-spare-parts",
    "https://www.cqswautoparts.com/byd/",
    "https://www.cqswautoparts.com/byd-spare-parts",
]:
    try:
        resp = client.get(url)
        print(f"  {resp.status_code} - {url}")
    except Exception as e:
        print(f"  ERROR - {url}: {e}")

# 2. CQSW main page - look for BYD model links
print("\n=== CQSW Main Page BYD Links ===")
try:
    html = client.get("https://www.cqswautoparts.com/").text
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        text = a.get_text(strip=True)
        if "byd" in href.lower() or "byd" in text.lower():
            print(f"  {text[:60]:<60} -> {href}")
except Exception as e:
    print(f"  ERROR: {e}")

# 3. Toyota spare parts site
print("\n=== Toyota Spare Parts - bZ4X ===")
try:
    resp = client.get("https://www.toyota-spare-parts.com/toyota-cars/BZ4X")
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        # Look for category links or part listings
        links = soup.find_all("a", href=True)
        bz4x_links = [a for a in links if "bz4x" in a.get("href", "").lower()]
        print(f"  bZ4X-related links: {len(bz4x_links)}")
        for a in bz4x_links[:15]:
            print(f"    {a.get_text(strip=True)[:50]} -> {a['href']}")
except Exception as e:
    print(f"  ERROR: {e}")

client.close()
print("\nDone.")
