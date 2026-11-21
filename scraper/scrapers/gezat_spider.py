"""Gezat: electric vehicle listing cards.

Ported from the ev3 ``collect/gezat.py`` collector. Listing cards are parsed from
their ordered text pieces: price | currency | year | make | model |
"mileage · fuel · gearbox" | location.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import guarded_get, now_utc

logger = logging.getLogger(__name__)


class GezatSpider(BaseScraper):
    """Gezat electric-vehicle listings (Addis Ababa market)."""

    name = "gezat"
    base_url = "https://gezat.et/cars-for-sale/electric"

    @staticmethod
    def card_to_row(card) -> Dict[str, Any]:
        """Convert a ``a.gl-card`` tag into a flat listing row."""
        pieces = [text for text in card.stripped_strings if text != "View details"]

        def piece(number: int) -> str:
            return pieces[number] if len(pieces) > number else ""

        specs = [part.strip() for part in piece(5).split("·")]
        href = card.get("href", "")

        return {
            "listing_id": href.split("/")[-1],
            "listing_url": "https://gezat.et" + href,
            "price_text": piece(0),
            "currency": piece(1),
            "year": piece(2),
            "make": piece(3),
            "model": piece(4),
            "mileage_text": specs[0] if len(specs) > 0 else "",
            "fuel_type": specs[1] if len(specs) > 1 else "",
            "transmission": specs[2] if len(specs) > 2 else "",
            "location": piece(6),
            "card_text_raw": " | ".join(pieces),
        }

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        page = 1

        while True:
            html = guarded_get(self, self.base_url, params={"page": page})
            if html is None:
                break

            soup = self.parse_soup(html)
            cards = soup.select("a.gl-card[href^='/listings/']")

            for card in cards:
                row = self.card_to_row(card)
                row["page"] = page
                row["collected_at_utc"] = now_utc()
                rows.append(row)

            print(f"  gezat page {page}  ({len(cards)} cards)")

            has_next_page = soup.select_one(f"a[href*='page={page + 1}']") is not None
            if not cards or not has_next_page:
                break
            if max_pages is not None and page >= max_pages:
                break
            page += 1

        return rows
