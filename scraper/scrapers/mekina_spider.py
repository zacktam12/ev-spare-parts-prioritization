"""Mekina.net: JSON search endpoint, electric cars only.

Ported from the ev3 ``collect/mekina.py`` collector.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import dig, guarded_get_json, now_utc

logger = logging.getLogger(__name__)


class MekinaSpider(BaseScraper):
    """Mekina.net electric-vehicle listings (Ethiopian marketplace)."""

    name = "mekina"
    base_url = "https://www.mekina.net/api/cars/search"
    FILTER = {"fuel": "Electric"}
    PAGE_SIZE = 50

    @staticmethod
    def remove_personal_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Blank seller name, phone and social links before persisting."""
        for vehicle in data.get("vehicles", []):
            seller = dig(vehicle, "car", "attributes", "seller")
            if isinstance(seller, dict):
                seller["name"] = "[removed]"
                seller["phone"] = "[removed]"
                seller["social_media"] = "[removed]"
        return data

    @staticmethod
    def vehicle_to_row(vehicle: Dict[str, Any]) -> Dict[str, Any]:
        car = dig(vehicle, "car", "attributes") or {}
        specs = car.get("car_ch") or {}

        return {
            "listing_id": car.get("displayId"),  # internal "id" can be negative
            "listing_url": "https://www.mekina.net/cars/" + (vehicle.get("permalink") or ""),
            "title": car.get("title"),
            "make": dig(specs, "brand", "data", "attributes", "name"),
            "model": dig(specs, "model", "data", "attributes", "name"),
            "year": specs.get("year_made"),
            "fuel_type": specs.get("fuel"),
            "transmission": specs.get("transmission"),
            "mileage_km": specs.get("mileage"),
            "color": specs.get("color"),
            "body_type": dig(specs, "body_type", "data", "attributes", "type"),
            "price_value": dig(car, "price", "price"),
            "currency": dig(car, "price", "currency"),
            "price_type": dig(car, "price", "price_type", "data", "attributes", "type"),
            "seller_type": dig(car, "seller", "seller_type", "data", "attributes", "type"),
            "location": car.get("location"),
            "status": car.get("status"),
            "created_at": car.get("createdAt"),
            "published_at": car.get("car_publication_date"),
            "updated_at": car.get("updatedAt"),
            "expires_at": car.get("car_expiration_date"),
            "visits": car.get("visits"),
            "is_featured": car.get("featured"),
            "is_premium": car.get("premium"),
        }

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        page = 1

        while True:
            params = {"page": page, "pageSize": self.PAGE_SIZE}
            params.update(self.FILTER)

            data = guarded_get_json(self, self.base_url, params=params)
            if data is None:
                break
            data = self.remove_personal_data(data)

            vehicles = data.get("vehicles", [])
            page_count = dig(data, "pagination", "pageCount") or 1

            for vehicle in vehicles:
                row = self.vehicle_to_row(vehicle)
                row["search_total_reported"] = data.get("total")
                row["page"] = page
                row["collected_at_utc"] = now_utc()
                rows.append(row)

            print(f"  mekina page {page}/{page_count}  ({len(vehicles)} listings)")

            if not vehicles or page >= page_count:
                break
            if max_pages is not None and page >= max_pages:
                break
            page += 1

        return rows
