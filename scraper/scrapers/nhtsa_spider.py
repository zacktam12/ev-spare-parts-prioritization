"""NHTSA (US): owner complaints and recalls by model year.

Ported from the ev3 ``collect/nhtsa.py`` collector. Both record types share one
column set so they can be persisted as a single table; ``record_type`` distinguishes
them. This is safety *context* only — the platform, not the local Ethiopian market.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_scraper import BaseScraper
from ._util import guarded_get_json, now_utc, remove_contact_details, dig

logger = logging.getLogger(__name__)


class NhtsaSpider(BaseScraper):
    """NHTSA owner complaints and recall campaigns for the selected platforms."""

    name = "nhtsa"
    base_url = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
    COMPLAINTS_URL = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
    RECALLS_URL = "https://api.nhtsa.gov/recalls/recallsByVehicle"

    # ID.4 stands in for the ID.6 (same MEB platform, not sold in the US).
    VEHICLES = [
        ("TOYOTA", "BZ4X", [2023, 2024, 2025]),
        ("VOLKSWAGEN", "ID.4", [2021, 2022, 2023, 2024, 2025]),
    ]

    FIELDNAMES = [
        "record_type", "make", "model", "model_year", "ref_number",
        "date_filed", "report_date", "components", "component",
        "summary", "crash", "fire", "collected_at_utc",
    ]

    @classmethod
    def complaint_row(cls, make: str, model: str, year: int, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "record_type": "complaint", "make": make, "model": model, "model_year": year,
            "ref_number": item.get("odiNumber"), "date_filed": item.get("dateComplaintFiled"),
            "report_date": "", "components": item.get("components"), "component": "",
            "summary": remove_contact_details(item.get("summary")),
            "crash": item.get("crash"), "fire": item.get("fire"),
            "collected_at_utc": now_utc(),
        }

    @classmethod
    def recall_row(cls, make: str, model: str, year: int, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "record_type": "recall", "make": make, "model": model, "model_year": year,
            "ref_number": item.get("NHTSACampaignNumber"), "date_filed": "",
            "report_date": item.get("ReportReceivedDate"), "components": "",
            "component": item.get("Component"), "summary": item.get("Summary"),
            "crash": "", "fire": "", "collected_at_utc": now_utc(),
        }

    def scrape(self, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []

        for make, model, years in self.VEHICLES:
            for year in years:
                params = {"make": make, "model": model, "modelYear": year}

                payload = guarded_get_json(self, self.COMPLAINTS_URL, params=params)
                complaints = (dig(payload, "results") or []) if payload else []
                rows.extend(self.complaint_row(make, model, year, item) for item in complaints)

                payload = guarded_get_json(self, self.RECALLS_URL, params=params)
                recalls = (dig(payload, "results") or []) if payload else []
                rows.extend(self.recall_row(make, model, year, item) for item in recalls)

                print(f"  nhtsa  {model} {year}: {len(complaints)} complaints, {len(recalls)} recalls")

        return rows
