"""evprotec (Dubai): VW ID.4 / ID.6 parts from the public WooCommerce store API.

Ported from the ev3 ``collect/evprotec.py`` collector.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import dig, guarded_get_json, now_utc

logger = logging.getLogger(__name__)


class EvprotecSpider(BaseScraper):
    """evprotec.com VW ID.4 / ID.6 parts (WooCommerce store API)."""

    name = "evprotec"
    base_url = "https://evprotec.com/wp-json/wc/store/v1/products"
    CATEGORIES = {417: "vw-id4", 418: "vw-id6", 664: "vw-id6-x"}

    @staticmethod
    def product_to_row(product: Dict[str, Any], category: str) -> Dict[str, Any]:
        prices = product.get("prices") or {}
        minor = prices.get("currency_minor_unit") or 0
        price = int(prices["price"]) / 10 ** minor if prices.get("price") else None

        return {
            "product_id": product.get("id"),
            "sku": product.get("sku"),
            "name": product.get("name"),
            "category": category,
            "price": price,
            "currency": prices.get("currency_code"),
            "in_stock": product.get("is_in_stock"),
            "stock_text": dig(product, "stock_availability", "text"),
            "product_url": product.get("permalink"),
            "collected_at_utc": now_utc(),
        }

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []

        for category_id, category in self.CATEGORIES.items():
            page = 1
            while True:
                params = {"category": category_id, "per_page": 100, "page": page}
                products = guarded_get_json(self, self.base_url, params=params)
                if products is None:
                    break
                if not products:
                    break

                for product in products:
                    rows.append(self.product_to_row(product, category))
                print(f"  evprotec  {category:<10} page {page}  ({len(products)} products)")

                if max_pages is not None and page >= max_pages:
                    break
                page += 1

        return rows
