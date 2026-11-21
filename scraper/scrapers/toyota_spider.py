import re
import json
import time
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

from .base_scraper import BaseScraper
from storage import DataExporter

logger = logging.getLogger(__name__)


class ToyotaBZ4XSpider(BaseScraper):
    """
    Scraper for Toyota bZ4X spare parts from toyota-spare-parts.com.
    Extracts OEM part numbers, descriptions, and prices for the 10 target
    EV import categories from the official Toyota parts catalogue.
    """

    name = "toyota"
    base_url = "https://www.toyota-spare-parts.com"

    # Map Toyota catalogue group names to our 10 target categories
    GROUP_TO_CATEGORY = {
        "FRONT DISC BRAKE CALIPER & DUST COVER": "Brake pads",
        "REAR DISC BRAKE CALIPER & DUST COVER": "Brake pads",
        "FRONT SPRING & SHOCK ABSORBER": "Shock absorbers",
        "REAR SPRING & SHOCK ABSORBER": "Shock absorbers",
        "FRONT BUMPER & BUMPER STAY": "Bumpers",
        "REAR BUMPER & BUMPER STAY": "Bumpers",
        "HOOD & FRONT FENDER": "Fenders/body panels",
        "FRONT FENDER APRON & DASH PANEL": "Fenders/body panels",
        "FRONT DOOR PANEL & GLASS": "Fenders/body panels",
        "REAR DOOR PANEL & GLASS": "Fenders/body panels",
        "BACK DOOR PANEL & GLASS": "Fenders/body panels",
        "HEADLAMP": "Headlights",
        "REAR COMBINATION LAMP": "Tail lights",
        "SIDE TURN SIGNAL LAMP & OUTER MIRROR LAMP": "Side mirrors",
        "MIRROR": "Side mirrors",
        "WINDSHIELD WIPER": "Wiper blades",
    }

    # Category URLs to scrape (one chassis variant, covering key part groups)
    # Using XEAM10L-MWDHSW (2023, FWD variant)
    CATEGORY_URLS = {
        "Brake pads": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928",  # Front disc brake
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73929",  # Rear disc brake
        ],
        "Brake discs": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73928",  # Front disc brake (discs listed here too)
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73929",  # Rear disc brake
        ],
        "Shock absorbers": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73935",  # Front spring & shock
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73936",  # Rear spring & shock
        ],
        "Bumpers": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73940",  # Front bumper
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73943",  # Rear bumper
        ],
        "Headlights": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74026",  # Headlamp
        ],
        "Tail lights": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0002/74031",  # Rear combination lamp
        ],
        "Side mirrors": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74109",  # Mirror
        ],
        "Fenders/body panels": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/73945",  # Hood & front fender
        ],
        "Wiper blades": [
            "/toyota-cars/BZ4X/2023/BZ4X/XEAM10L-MWDHSW/561210//0001/74093",  # Windshield wiper
        ],
        # Cabin-air filter not in direct catalogue group names — will be searched separately
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.review_items: List[Dict[str, Any]] = []

    def _extract_parts_from_page(self, html: str, category: str, page_url: str, collection_date: str) -> List[Dict[str, Any]]:
        """Extract part rows from a Toyota catalogue group page."""
        soup = self.parse_soup(html)
        results = []

        # Toyota parts pages use table rows for parts
        rows = soup.select("table tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            # Extract text from all cells
            cell_texts = [c.get_text(strip=True) for c in cells]
            combined = " ".join(cell_texts).lower()

            # Look for part number pattern (Toyota OEM: usually format like 04465-42250)
            part_numbers = re.findall(r'\b\d{5}[-–]\d{5}\b', " ".join(cell_texts))
            if not part_numbers:
                # Also try format without dash
                part_numbers = re.findall(r'\b[A-Z0-9]{10,15}\b', " ".join(cell_texts))

            # Extract description
            description = ""
            for text in cell_texts:
                if len(text) > 5 and not re.match(r'^[\d\-\.]+$', text):
                    description = text
                    break

            # Extract price if present
            price = None
            currency = None
            for text in cell_texts:
                price_match = re.search(r'[\$€£¥]?\s*([\d,]+(?:\.\d{2})?)', text)
                if price_match and len(price_match.group(1)) > 1:
                    try:
                        price = float(price_match.group(1).replace(",", ""))
                        if "$" in text or "USD" in text.upper():
                            currency = "USD"
                        elif "€" in text or "EUR" in text.upper():
                            currency = "EUR"
                    except ValueError:
                        pass

            if part_numbers or (description and len(description) > 3):
                record = {
                    "product_name": description,
                    "part_number": part_numbers[0] if part_numbers else "",
                    "oe_number": part_numbers[0] if part_numbers else "",
                    "vehicle_compatibility": "Toyota bZ4X 2023 (XEAM10L)",
                    "category": category,
                    "price": price,
                    "currency": currency,
                    "availability_status": "Listed in OEM catalogue",
                    "raw_price": "",
                    "product_url": page_url,
                    "source_url": self.base_url,
                    "collection_date": collection_date,
                }
                results.append(record)

        # Also try to extract from links with part numbers
        links = soup.find_all("a", href=True)
        seen_hrefs = set()
        for a in links:
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if href in seen_hrefs:
                continue
            seen_hrefs.add(href)

            # Look for part detail links
            part_match = re.search(r'/(\d{5}[-–]\d{5})', href + " " + text)
            if part_match and len(text) > 2:
                pn = part_match.group(1)
                record = {
                    "product_name": text,
                    "part_number": pn,
                    "oe_number": pn,
                    "vehicle_compatibility": "Toyota bZ4X 2023 (XEAM10L)",
                    "category": category,
                    "price": None,
                    "currency": None,
                    "availability_status": "Listed in OEM catalogue",
                    "raw_price": "",
                    "product_url": self.base_url + href if href.startswith("/") else href,
                    "source_url": page_url,
                    "collection_date": collection_date,
                }
                # Avoid duplicate part numbers
                if pn not in [r["part_number"] for r in results]:
                    results.append(record)

        return results

    def scrape(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrapes Toyota bZ4X parts catalogue for 10 target categories.
        """
        collection_date = datetime.now().strftime("%Y-%m-%d")
        print(f"[*] Starting Toyota bZ4X parts scraper...")

        all_results: List[Dict[str, Any]] = []
        seen_parts = set()
        pages_scraped = 0

        for category, urls in self.CATEGORY_URLS.items():
            print(f"\n[*] Scraping category: {category}")
            category_parts = []

            for url_path in urls:
                full_url = self.base_url + url_path
                print(f"    Fetching: ...{url_path[-50:]}")

                try:
                    html = self.fetch_html(full_url)
                    pages_scraped += 1
                    parts = self._extract_parts_from_page(html, category, full_url, collection_date)

                    for p in parts:
                        key = (p["part_number"], p["category"])
                        if key not in seen_parts:
                            seen_parts.add(key)
                            category_parts.append(p)

                    time.sleep(1.0)  # Politeness delay
                except Exception as e:
                    logger.error(f"Failed to scrape {full_url}: {e}")
                    print(f"    [!] Error: {e}")

            all_results.extend(category_parts)
            print(f"    -> {len(category_parts)} unique parts found for {category}")

        # Summary
        print(f"\n[✔] Toyota bZ4X Scraping Completed:")
        print(f"    - Pages scraped: {pages_scraped}")
        print(f"    - Total unique parts: {len(all_results)}")

        # Category breakdown
        cat_counts = {}
        for r in all_results:
            cat_counts[r["category"]] = cat_counts.get(r["category"], 0) + 1
        for cat, count in sorted(cat_counts.items()):
            print(f"    - {cat}: {count} parts")

        # Export
        if all_results:
            DataExporter.to_csv(all_results, "outputs/toyota_bz4x.csv")
            DataExporter.to_json(all_results, "outputs/toyota_bz4x.json")
            print(f"  [+] Saved to: outputs/toyota_bz4x.csv and outputs/toyota_bz4x.json")

        return all_results
