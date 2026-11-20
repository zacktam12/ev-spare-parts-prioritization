import re
import time
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

try:
    import certifi
    SSL_VERIFY_PATH = certifi.where()
except ImportError:
    SSL_VERIFY_PATH = True

from .base_scraper import BaseScraper
from storage import DataExporter

logger = logging.getLogger(__name__)

class AdeyMarketSpider(BaseScraper):
    """
    Scraper for Adey Market Ethiopian Electric Vehicle marketplace.
    Target: https://adey-market.com/categories/cars?type=cars_electric
    Extracts public electric vehicle listings, focusing on the 5 candidate vehicles:
      1. BYD Seagull
      2. BYD Yuan Up
      3. Changan Benben E-Star
      4. Toyota bZ4X
      5. Volkswagen ID.4 / ID.6
    Preserves raw extractions and produces normalized vehicle evidence.
    """

    name = "adey"
    base_url = "https://adey-market.com/categories/cars?type=cars_electric"

    # Dedicated brand/model category endpoints for deep candidate discovery
    TARGET_ENDPOINTS = [
        ("BYD Seagull", "https://adey-market.com/categories/cars/byd-seagull-dolphin-mini-atto-1"),
        ("BYD Yuan Up", "https://adey-market.com/categories/cars/byd-yuan-up-atto-2"),
        ("Toyota bZ4X", "https://adey-market.com/categories/cars/toyota-bz-series-bz4x-bz3-bz3x-bz5"),
        ("Volkswagen ID.4 Crozz", "https://adey-market.com/categories/cars/volkswagen-id-4-crozz-faw-vw"),
        ("Volkswagen ID.4", "https://adey-market.com/categories/cars/volkswagen-id-4"),
        ("Changan Benben E-Star", "https://adey-market.com/categories/cars/changan-benben-e-star"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Re-configure client to use certifi bundle for robust SSL verification
        self.client.close()
        import httpx
        from config import config
        self.client = httpx.Client(
            headers=config.random_headers,
            timeout=self.timeout,
            verify=SSL_VERIFY_PATH,
            follow_redirects=True,
        )
        self.raw_listings: List[Dict[str, Any]] = []
        self.cleaned_listings: List[Dict[str, Any]] = []

    def classify_candidate_vehicle(self, title: str) -> Tuple[str, str]:
        """
        Identifies vehicle make and model strictly for the 5 target candidates.
        Returns: (vehicle_make, vehicle_model) or ('', '')
        """
        tl = title.lower()
        if "seagull" in tl or "dolphin mini" in tl:
            return "BYD", "Seagull"
        elif "yuan up" in tl or "yuan-up" in tl or "yuanup" in tl:
            return "BYD", "Yuan Up"
        elif "benben" in tl or "e-star" in tl or "estar" in tl:
            return "Changan", "Benben E-Star"
        elif "bz4x" in tl or "bz 4x" in tl:
            return "Toyota", "bZ4X"
        elif "id.4" in tl or "id4" in tl or "id 4" in tl:
            return "Volkswagen", "ID.4"
        elif "id.6" in tl or "id6" in tl or "id 6" in tl:
            return "Volkswagen", "ID.6"
        return "", ""

    def parse_card(self, title: str, raw_price: str, meta_str: str, listing_url: str, source_url: str, collection_date: str) -> Dict[str, Any]:
        """
        Extracts structured fields from an individual card.
        """
        # Price and currency extraction
        price_clean = raw_price.strip()
        listed_price = ""
        currency = ""
        if "ETB" in price_clean.upper() or "BIRR" in price_clean.upper():
            currency = "ETB"
        elif "$" in price_clean or "USD" in price_clean.upper():
            currency = "USD"

        match_num = re.search(r"([\d,]+(?:\.\d+)?)", price_clean)
        if match_num:
            clean_num_str = match_num.group(1).replace(",", "")
            try:
                listed_price = float(clean_num_str)
            except ValueError:
                pass

        # Meta extraction (seller, location, listing_date)
        parts = [p.strip() for p in re.split(r"[·|•]", meta_str) if p.strip()]
        seller_name = ""
        location = ""
        listing_date = ""

        for i, p in enumerate(parts):
            if any(w in p.lower() for w in ["ago", "yesterday", "today", "min", "hour", "day", "nov", "oct", "dec", "jan", "feb", "2026", "2025", "2024"]):
                listing_date = p
            elif any(loc.lower() in p.lower() for loc in ["addis", "ababa", "hawassa", "adama", "dire", "bahir", "ethiopia"]):
                location = p
            elif i == 0:
                seller_name = p
            elif not location and not any(w in p.lower() for w in ["ago", "min", "h", "d"]):
                location = p

        # Model year (only if explicitly stated, e.g. 2018-2027)
        model_year = ""
        year_match = re.search(r"\b(201[89]|202[0-7])\b", title)
        if year_match:
            model_year = int(year_match.group(1))

        # Classification
        make, model = self.classify_candidate_vehicle(title)

        return {
            "listing_title": title,
            "vehicle_make": make,
            "vehicle_model": model,
            "model_year": model_year,
            "listed_price": listed_price,
            "currency": currency,
            "seller_name": seller_name,
            "location": location,
            "listing_date": listing_date,
            "listing_url": listing_url,
            "source_url": source_url,
            "collection_date": collection_date,
            "raw_price": raw_price,
            "raw_meta": meta_str,
        }

    def scrape(self, max_pages: int = 3) -> List[Dict[str, Any]]:
        """
        Scrapes Adey Market for the 5 target candidate vehicles.
        Scrapes general electric car category pages and candidate-specific model pages.
        Exports outputs/adey_raw.csv, outputs/adey_raw.json, and outputs/adey_cleaned.csv.
        """
        collection_date = datetime.now().strftime("%Y-%m-%d")
        print(f"[*] Starting Adey Market electric vehicle scraper (max_pages per endpoint: {max_pages})...")

        seen_urls = set()
        self.raw_listings = []
        self.cleaned_listings = []
        pages_inspected = 0
        total_cards_scanned = 0
        duplicates_avoided = 0
        extraction_failures = 0

        # Construct target endpoints to visit:
        # 1. Main cars_electric category pages (up to max_pages)
        endpoints = []
        for p in range(1, max_pages + 1):
            url = f"{self.base_url}&page={p}" if p > 1 else self.base_url
            endpoints.append(("General EV Category", url))

        # 2. Dedicated candidate model endpoints (up to 2 pages each)
        for label, model_url in self.TARGET_ENDPOINTS:
            for p in range(1, min(max_pages, 2) + 1):
                url = f"{model_url}?page={p}" if p > 1 else model_url
                endpoints.append((label, url))

        for source_label, endpoint_url in endpoints:
            pages_inspected += 1
            print(f"[*] Inspecting page {pages_inspected}/{len(endpoints)}: [{source_label}] {endpoint_url}")
            try:
                html = self.fetch_html(endpoint_url)
                soup = self.parse_soup(html)
                cards = soup.select("a.pcard")
                total_cards_scanned += len(cards)

                for card in cards:
                    try:
                        href = card.get("href", "")
                        if not href:
                            continue
                        full_url = urljoin(self.base_url, href)

                        if full_url in seen_urls:
                            duplicates_avoided += 1
                            continue
                        seen_urls.add(full_url)

                        title_elem = card.select_one(".pcard-title")
                        title = title_elem.get_text(strip=True) if title_elem else ""

                        price_elem = card.select_one(".pcard-price")
                        raw_price = price_elem.get_text(strip=True) if price_elem else ""

                        meta_elem = card.select_one(".pcard-meta")
                        raw_meta = meta_elem.get_text(" · ", strip=True) if meta_elem else ""

                        record = self.parse_card(
                            title=title,
                            raw_price=raw_price,
                            meta_str=raw_meta,
                            listing_url=full_url,
                            source_url=endpoint_url,
                            collection_date=collection_date,
                        )

                        self.raw_listings.append(record)

                        # Filter for the cleaned dataset (the 5 candidate vehicles)
                        if record["vehicle_make"] and record["vehicle_model"]:
                            clean_rec = {
                                "listing_title": record["listing_title"],
                                "vehicle_make": record["vehicle_make"],
                                "vehicle_model": record["vehicle_model"],
                                "model_year": record["model_year"],
                                "listed_price": record["listed_price"],
                                "currency": record["currency"],
                                "seller_name": record["seller_name"],
                                "location": record["location"],
                                "listing_date": record["listing_date"],
                                "listing_url": record["listing_url"],
                                "source_url": record["source_url"],
                                "collection_date": record["collection_date"],
                            }
                            self.cleaned_listings.append(clean_rec)

                    except Exception as err:
                        extraction_failures += 1
                        logger.error(f"Error parsing card on {endpoint_url}: {err}")

            except Exception as e:
                logger.error(f"Failed to fetch {endpoint_url}: {e}")

        # Summary statistics
        print(f"\n[✔] Adey Market Scraping Completed:")
        print(f"    - Pages inspected: {pages_inspected}")
        print(f"    - Total cards scanned: {total_cards_scanned}")
        print(f"    - Unique raw listings collected: {len(self.raw_listings)}")
        print(f"    - Duplicate listings avoided: {duplicates_avoided}")
        print(f"    - Target candidate EV listings (cleaned): {len(self.cleaned_listings)}")
        print(f"    - Extraction failures: {extraction_failures}")

        # Export outputs
        DataExporter.to_csv(self.raw_listings, "outputs/adey_raw.csv")
        DataExporter.to_json(self.raw_listings, "outputs/adey_raw.json")
        DataExporter.to_csv(self.cleaned_listings, "outputs/adey_cleaned.csv")
        DataExporter.to_json(self.cleaned_listings, "outputs/adey_cleaned.json")

        print(f"  [+] Saved raw extractions to: outputs/adey_raw.csv and outputs/adey_raw.json")
        print(f"  [+] Saved cleaned candidate dataset to: outputs/adey_cleaned.csv and outputs/adey_cleaned.json")

        return self.cleaned_listings
