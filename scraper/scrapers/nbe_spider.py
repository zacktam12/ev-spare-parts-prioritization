"""National Bank of Ethiopia: official daily exchange rates (latest day with data).

Ported from the ev3 ``collect/nbe.py`` collector. Steps back up to
``LOOKBACK_DAYS`` calendar days because weekends and public holidays carry no rates.
"""

import logging
from datetime import date, timedelta
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import guarded_get_json, now_utc

logger = logging.getLogger(__name__)


class NbeRatesSpider(BaseScraper):
    """National Bank of Ethiopia official exchange rates (ETB buying / selling)."""

    name = "nbe"
    base_url = "https://api.nbe.gov.et/api/filter-exchange-rates"
    LOOKBACK_DAYS = 10

    @staticmethod
    def rate_rows(payload: Any) -> List[Dict[str, Any]]:
        """Convert the NBE JSON payload into flat rate rows."""
        rates = (payload or {}).get("data", []) if isinstance(payload, dict) else []
        return [{
            "rate_date": item.get("date"),
            "currency": (item.get("currency") or {}).get("code"),
            "currency_name": (item.get("currency") or {}).get("name"),
            "buying_etb": item.get("buying"),
            "selling_etb": item.get("selling"),
            "weighted_average_etb": item.get("weighted_average"),
            "collected_at_utc": now_utc(),
        } for item in rates]

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        day = date.today()
        for _ in range(self.LOOKBACK_DAYS):
            payload = guarded_get_json(self, self.base_url, params={"date": day.isoformat()})
            rows = self.rate_rows(payload)
            if rows:
                print(f"  nbe  {len(rows)} rates for {day.isoformat()}")
                return rows
            day = day - timedelta(days=1)

        logger.warning("NBE returned no rates within the lookback window")
        return []
