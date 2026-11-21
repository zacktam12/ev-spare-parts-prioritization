"""AfroMekina: JSON filter endpoint, electric cars only.

Ported from the ev3 ``collect/afromekina.py`` collector.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import dig, guarded_get_json, now_utc, remove_contact_details

logger = logging.getLogger(__name__)


class AfroMekinaSpider(BaseScraper):
    """AfroMekina electric-vehicle listings (Ethiopian marketplace)."""

    name = "afromekina"
    base_url = "https://api.afromekina.com/api/listings/filter"
    FILTER = {"fuel_type": "electric", "per_page": 24}
    PERSONAL_FIELDS = ["user", "phone", "seller_phone", "description"]

    @classmethod
    def remove_personal_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove seller contact details; keep only dealership id and name."""
        for listing in dig(data, "data", "listings") or []:
            for field in cls.PERSONAL_FIELDS:
                if field in listing:
                    listing[field] = "[removed]"
            dealership = listing.get("dealership")
            if isinstance(dealership, dict):
                listing["dealership"] = {"id": dealership.get("id"), "name": dealership.get("name")}
        return data

    @staticmethod
    def listing_url(listing: Dict[str, Any]) -> str:
        """e.g. https://afromekina.com/cars/changan-q05-2026-13709"""
        words = f"{listing.get('brand')} {listing.get('model')} {listing.get('year')}".lower().split()
        return "https://afromekina.com/cars/" + "-".join(words) + f"-{listing.get('id')}"

    @classmethod
    def listing_to_row(cls, listing: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "listing_id": listing.get("id"),
            "listing_url": cls.listing_url(listing),
            "title": remove_contact_details(listing.get("title")),
            "make": listing.get("brand"),
            "model": listing.get("model"),
            "trim": listing.get("trim"),
            "year": listing.get("year"),
            "fuel_type": listing.get("fuel_type"),
            "condition": listing.get("condition"),
            "transmission": listing.get("transmission"),
            "body_type": listing.get("body_type"),
            "mileage_km": listing.get("mileage"),
            "price_value": listing.get("price"),
            "currency": listing.get("currency"),
            "price_type": listing.get("price_type"),
            "has_bank_loan": listing.get("has_bank_loan"),
            "seller_type": listing.get("role_type"),
            "seller_account_id": listing.get("user_id"),
            "dealership_name": dig(listing, "dealership", "name"),
            "location": listing.get("location"),
            "status": listing.get("status"),
            "created_at": listing.get("created_at"),
            "published_at": listing.get("published_at"),
            "updated_at": listing.get("updated_at"),
            "expires_at": listing.get("expires_at"),
            "views_count": listing.get("views_count"),
            "is_featured": listing.get("is_featured"),
        }

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        page = 1

        while True:
            params = {"page": page}
            params.update(self.FILTER)

            data = guarded_get_json(self, self.base_url, params=params)
            if data is None:
                break
            data = self.remove_personal_data(data)

            listings = dig(data, "data", "listings") or []
            pagination = dig(data, "data", "pagination") or {}
            last_page = pagination.get("last_page") or 1

            for listing in listings:
                row = self.listing_to_row(listing)
                row["search_total_reported"] = pagination.get("total")
                row["page"] = page
                row["collected_at_utc"] = now_utc()
                rows.append(row)

            print(f"  afromekina page {page}/{last_page}  ({len(listings)} listings)")

            if not listings or page >= last_page:
                break
            if max_pages is not None and page >= max_pages:
                break
            page += 1

        return rows
