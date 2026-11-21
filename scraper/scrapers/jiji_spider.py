"""Jiji Ethiopia: JSON listing endpoint, one run per configured search.

Ported from the ev3 ``collect/jiji.py`` collector. Two modes are kept:
``scrape`` for the vehicles section and ``scrape_parts`` for
car-parts-and-accessories (English and Amharic part queries).
"""

import logging
import re
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import dig, guarded_get_json, now_utc, remove_contact_details

logger = logging.getLogger(__name__)


class JijiSpider(BaseScraper):
    """Jiji Ethiopia listings via its public JSON search endpoint."""

    name = "jiji"
    base_url = "https://jiji.com.et/api_web/v1/listing"

    # label -> search parameters (vehicles)
    SEARCHES = {
        "filter: powertrain=Electric": {"filter_attr_7177_powertrain": "Electric"},
        "seagull": {"query": "seagull"},
        "yuan up": {"query": "yuan up"},
        "e-star": {"query": "e-star"},
        "benben": {"query": "benben"},
        "bz4x": {"query": "bz4x"},
        "id.4": {"query": "id.4"},
        "id.6": {"query": "id.6"},
        "yuan plus": {"query": "yuan plus"},
        "sealion": {"query": "sealion"},
        "song plus": {"query": "song plus"},
        "byd e2": {"query": "byd e2"},
        "dolphin": {"query": "dolphin"},
        "bz3": {"query": "bz3"},
    }

    # label -> search text (parts; vehicles + part words in English and Amharic)
    PARTS_SEARCHES = {
        "id4": "id4", "id6": "id6", "bz4x": "bz4x", "yuan up": "yuan up", "atto 2": "atto 2",
        "brake pad": "brake pad", "brake disc": "brake disc", "shock absorber": "shock absorber",
        "suspension": "suspension", "headlight": "headlight", "head light": "head light",
        "tail light": "tail light", "side mirror": "side mirror", "bumper": "bumper", "fender": "fender",
        "tire": "tire", "tyre": "tyre", "car battery": "car battery", "12v battery": "12v battery",
        "am: brake pad": "ፍሬን ሸራ", "am: bumper": "ፓራወልት", "am: fender": "ፈረፋንጎ",
        "am: shock absorber": "አሞርዛተር", "am: light": "ማብራት", "am: tyre": "ጎማ", "am: battery": "ባትሪ",
    }

    @staticmethod
    def advert_to_row(advert: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single Jiji advert payload into a flat row."""
        attrs = {item.get("name"): item.get("value") for item in advert.get("attrs") or []}
        schema = advert.get("schema_org") or {}

        return {
            "listing_id": advert.get("id"),
            "listing_url": "https://jiji.com.et" + (advert.get("url") or ""),
            "title": remove_contact_details(advert.get("title")),
            "price_value": dig(advert, "price_obj", "value"),
            "price_text": advert.get("price_title"),
            "make": dig(schema, "brand", "name"),
            "model": schema.get("model"),
            "year": schema.get("vehicleModelDate"),
            "color": schema.get("color"),
            "condition": attrs.get("Condition"),
            "transmission": attrs.get("Transmission"),
            "mileage_km": attrs.get("Mileage"),
            "fuel_type": schema.get("fuelType"),
            "region": advert.get("region_name"),
            "region_parent": advert.get("region_parent_name"),
            "seller_account_id": advert.get("user_id"),
            "is_boosted": advert.get("is_boost"),
            "listing_age_label": "; ".join(str(label.get("value")) for label in advert.get("labels") or []),
        }

    def _search(self, label: str, extra_params: Dict[str, Any], max_pages: Optional[int],
                slug: str) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        page = 1

        while True:
            params = {"slug": slug, "page": page}
            params.update(extra_params)

            data = guarded_get_json(self, self.base_url, params=params)
            if data is None:
                break

            adverts = dig(data, "adverts_list", "adverts") or []
            total = dig(data, "adverts_list", "count")

            for advert in adverts:
                row = self.advert_to_row(advert)
                row["search_label"] = label
                row["search_total_reported"] = total
                row["page"] = page
                row["collected_at_utc"] = now_utc()
                rows.append(row)

            safe_label = re.sub(r"\W+", "_", label).strip("_")
            print(f"  jiji[{slug}]  {safe_label:<28} page {page}  ({len(adverts)} ads, {total} reported)")

            if not adverts or not data.get("next_url"):
                break
            if max_pages is not None and page >= max_pages:
                break
            page += 1

        return rows

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """Vehicles section: one run per search in :attr:`SEARCHES`."""
        rows: List[Dict[str, Any]] = []
        for label, extra_params in self.SEARCHES.items():
            rows.extend(self._search(label, extra_params, max_pages, slug="cars"))
        return rows

    def scrape_parts(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """Car-parts section: one run per search in :attr:`PARTS_SEARCHES`."""
        rows: List[Dict[str, Any]] = []
        for label, query in self.PARTS_SEARCHES.items():
            rows.extend(self._search(label, {"query": query}, max_pages,
                                     slug="car-parts-and-accessories"))
        return rows
