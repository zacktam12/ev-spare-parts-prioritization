"""asiautos (China): BYD parts from the public Shopify product feed.

Ported from the ev3 ``collect/asiautos.py`` collector. Prices in the feed are
placeholders; part numbers are the signal. The store rate-limits aggressive
crawling, so the default request delay is raised to 15 seconds.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import guarded_get_json, now_utc

logger = logging.getLogger(__name__)


class AsiautosSpider(BaseScraper):
    """asiautos.net BYD parts (Shopify product feed)."""

    name = "asiautos"
    base_url = "https://asiautos.net/products.json"
    MAX_PAGES = 2  # newest products (incl. Yuan Up range) are on the first pages

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("delay", 15.0)  # store rate-limits below this
        super().__init__(*args, **kwargs)

    @staticmethod
    def product_to_row(product: Dict[str, Any]) -> Dict[str, Any]:
        variant = (product.get("variants") or [{}])[0]
        return {
            "product_id": product.get("id"),
            "title": product.get("title"),
            "product_type": product.get("product_type"),
            "tags": ", ".join(product.get("tags") or []),
            "price": variant.get("price"),
            "available": variant.get("available"),
            "product_url": "https://asiautos.net/products/" + (product.get("handle") or ""),
            "updated_at": product.get("updated_at"),
            "collected_at_utc": now_utc(),
        }

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        limit = max_pages if max_pages is not None else self.MAX_PAGES
        rows: List[Dict[str, Any]] = []
        page = 1

        while page <= limit:
            payload = guarded_get_json(self, self.base_url, params={"limit": 250, "page": page})
            if payload is None:
                break

            products = payload.get("products", [])
            if not products:
                break

            rows.extend(self.product_to_row(product) for product in products)
            print(f"  asiautos  page {page}  ({len(products)} products)")
            page += 1

        return rows
