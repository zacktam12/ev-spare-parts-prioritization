import re
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

from .base_scraper import BaseScraper
from storage import DataExporter

logger = logging.getLogger(__name__)

class LandinSpider(BaseScraper):
    """
    Scraper for Landin Parts BYD catalog (https://www.landinparts.com/byd/).
    Extracts BYD Seagull spare-parts listings, preserves exact compatibility labels,
    classifies parts into 10 target EV import categories, keeps uncertain parts
    in a review dataset, and excludes unrelated items.
    """

    name = "landin"
    base_url = "https://www.landinparts.com/byd/"

    # Target 10 categories required for EV spare-parts import prioritization
    TARGET_CATEGORIES = [
        "Brake pads",
        "Brake discs",
        "Cabin-air filters",
        "Wiper blades",
        "Headlights",
        "Tail lights",
        "Side mirrors",
        "Bumpers",
        "Fenders/body panels",
        "Shock absorbers",
    ]

    # Explicitly unrelated products to exclude from the main output
    EXCLUDE_KEYWORDS = [
        "logo",
        "car letters",
        "mud guard",
        "side skirts",
        "side skirt",
        "wheel hub",
        "wheel rim",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.review_items: List[Dict[str, Any]] = []
        self.excluded_items: List[Dict[str, Any]] = []

    def classify_product(self, name: str, data_cat: str) -> Tuple[str, Optional[str]]:
        """
        Classifies product into one of the 10 target categories, an EXCLUDED status,
        or an UNCERTAIN status for the review queue.
        Returns: (status, category_name) where status is in ('TARGET', 'EXCLUDED', 'UNCERTAIN')
        """
        nl = name.lower()
        cl = data_cat.lower() if data_cat else ""

        # Check explicit exclusions
        for excl in self.EXCLUDE_KEYWORDS:
            if excl in nl:
                return "EXCLUDED", None

        # 1. Brake pads
        if "brake pad" in nl:
            return "TARGET", "Brake pads"

        # 2. Brake discs
        if "brake disc" in nl:
            return "TARGET", "Brake discs"

        # 3. Cabin-air filters
        if "cabin" in nl or ("air" in nl and "filter" in nl):
            return "TARGET", "Cabin-air filters"

        # 4. Wiper blades (exclude wiper motors)
        if "wiper" in nl:
            if "motor" in nl:
                return "UNCERTAIN", None
            return "TARGET", "Wiper blades"

        # 5. Headlights
        if "head lamp" in nl or "headlamp" in nl or "headlight" in nl or cl == "head-lamps":
            return "TARGET", "Headlights"

        # 6. Tail lights
        if "tail lamp" in nl or "taillamp" in nl or "tail light" in nl or "taillight" in nl or cl == "tail-lamps":
            return "TARGET", "Tail lights"

        # 7. Side mirrors
        if "side mirror" in nl or "rearview mirror" in nl or cl == "side-mirrors":
            return "TARGET", "Side mirrors"

        # 8. Bumpers
        if "bumper" in nl or cl in ("front-bumper", "rear-bumper"):
            return "TARGET", "Bumpers"

        # 9. Fenders/body panels
        body_panel_keywords = [
            "fender", "door panel", "hood/bonnet", "hood", "rear body panel",
            "roof sheet metal", "tail gate"
        ]
        if any(k in nl for k in body_panel_keywords) or cl in ("fender", "door-panel", "hood-bonnet"):
            return "TARGET", "Fenders/body panels"

        # 10. Shock absorbers
        if "shock absorber" in nl or "shock abs" in nl or "air spring" in nl:
            return "TARGET", "Shock absorbers"

        return "UNCERTAIN", None

    def _parse_price(self, raw_price: str) -> Tuple[Optional[float], Optional[str], str]:
        """
        Parses raw price strings such as '¥198 RMB' or 'Price on request'.
        Returns: (price, currency, availability_status)
        """
        clean_p = raw_price.strip()
        if not clean_p or "request" in clean_p.lower():
            return None, None, "Price on request"

        # Check for currency symbols / codes (e.g. ¥198 RMB)
        currency = None
        if "rmb" in clean_p.upper() or "¥" in clean_p:
            currency = "RMB"
        elif "$" in clean_p or "USD" in clean_p.upper():
            currency = "USD"
        elif "EUR" in clean_p.upper() or "€" in clean_p:
            currency = "EUR"

        # Extract numeric portion
        match = re.search(r"([0-9]+(?:\.[0-9]+)?)", clean_p)
        if match:
            try:
                numeric_val = float(match.group(1))
                return numeric_val, currency, "In Stock"
            except ValueError:
                pass

        return None, currency, clean_p

    def scrape(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Executes scraping on Landin Parts BYD catalog.
        Extracts BYD Seagull items, sorts into target vs review,
        and saves landin_review.csv automatically.
        """
        collection_date = datetime.now().strftime("%Y-%m-%d")
        print(f"[*] Fetching Landin Parts catalog from {self.base_url}...")

        html = self.fetch_html(self.base_url)
        if not html:
            print("[!] Failed to obtain HTML from Landin Parts.")
            return []

        soup = self.parse_soup(html)
        cards = soup.select(".product-card-wrap")
        print(f"[*] Total product cards found in catalog: {len(cards)}")

        target_results: List[Dict[str, Any]] = []
        self.review_items = []
        self.excluded_items = []

        seen_product_urls = set()
        failed_extractions = 0

        for card in cards:
            try:
                # 1. Compatibility check: Restrict to BYD Seagull products
                model_elem = card.select_one(".model")
                vehicle_compatibility = model_elem.get_text(strip=True) if model_elem else ""

                # Button metadata (contains fallback/canonical structured product fields)
                btn = card.select_one(".add-cart-btn")
                data_item: Dict[str, Any] = {}
                if btn and btn.get("data-item"):
                    try:
                        import json
                        data_item = json.loads(btn["data-item"])
                    except Exception:
                        pass

                # Fallback to data_item if model_elem was empty
                if not vehicle_compatibility and data_item.get("m"):
                    vehicle_compatibility = data_item["m"].strip()

                if "seagull" not in vehicle_compatibility.lower():
                    continue  # Skip non-Seagull products

                # 2. Product URL & deduplication
                link_elem = card.select_one("a.product-card")
                rel_url = link_elem["href"] if link_elem and "href" in link_elem.attrs else data_item.get("u", "")
                if not rel_url:
                    failed_extractions += 1
                    logger.warning(f"Product card missing URL: {card}")
                    continue

                product_url = urljoin(self.base_url, rel_url)
                if product_url in seen_product_urls:
                    continue  # Prevent duplicates
                seen_product_urls.add(product_url)

                # 3. Product Name (clean name from structured payload or h3 text)
                product_name = data_item.get("n", "")
                if not product_name:
                    h3_elem = card.select_one("h3")
                    if h3_elem:
                        # Remove hot / lr badges
                        product_name = h3_elem.find(text=True, recursive=False)
                        product_name = product_name.strip() if product_name else h3_elem.get_text(strip=True)
                    else:
                        product_name = ""

                # 4. Part Number
                part_no = data_item.get("s", "")
                if not part_no:
                    sku_elem = card.select_one(".sku")
                    if sku_elem:
                        sku_text = sku_elem.get_text(strip=True)
                        part_no = re.sub(r"^Part\s*No:?\s*", "", sku_text, flags=re.IGNORECASE).strip()

                # 5. OE Number
                oe_number = data_item.get("o", "")
                if not oe_number:
                    oe_elem = card.select_one(".oe")
                    if oe_elem:
                        oe_text = oe_elem.get_text(strip=True)
                        oe_number = re.sub(r"^OE:?\s*", "", oe_text, flags=re.IGNORECASE).strip()

                # 6. Price, Currency, and Availability Status
                raw_price = data_item.get("p", "")
                if not raw_price:
                    price_elem = card.select_one(".price")
                    raw_price = price_elem.get_text(strip=True) if price_elem else ""

                price_val, currency_val, availability = self._parse_price(raw_price)

                # 7. Category classification
                data_cat = card.get("data-cat", "")
                status, assigned_category = self.classify_product(product_name, data_cat)

                record = {
                    "product_name": product_name,
                    "part_number": part_no,
                    "oe_number": oe_number,
                    "vehicle_compatibility": vehicle_compatibility,
                    "category": assigned_category,
                    "price": price_val,
                    "currency": currency_val,
                    "availability_status": availability,
                    "raw_price": raw_price,
                    "product_url": product_url,
                    "source_url": self.base_url,
                    "collection_date": collection_date,
                }

                if status == "TARGET":
                    target_results.append(record)
                elif status == "EXCLUDED":
                    self.excluded_items.append(record)
                else:
                    record["category"] = "Uncertain / Review"
                    self.review_items.append(record)

            except Exception as e:
                failed_extractions += 1
                logger.error(f"Error parsing product card: {e}")

        if failed_extractions > 0:
            print(f"[!] Warning: {failed_extractions} cards failed extraction.")

        print(f"[*] Extraction breakdown for BYD Seagull:")
        print(f"    - Target prioritized items: {len(target_results)}")
        print(f"    - Uncertain / review items: {len(self.review_items)}")
        print(f"    - Excluded unrelated items: {len(self.excluded_items)}")

        # Automatically export review items to outputs/landin_review.csv
        if self.review_items:
            DataExporter.to_csv(self.review_items, "outputs/landin_review.csv")
            print(f"  [+] Saved {len(self.review_items)} review items to: outputs/landin_review.csv")

        return target_results
