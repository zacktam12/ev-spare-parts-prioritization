"""Validation tests for the scraper package and the ported collectors.

These tests never touch the network: they exercise the registry wiring and the pure
payload-parsing helpers (the part of each spider most likely to rot when a source
changes its JSON/HTML shape).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SCRAPER_DIR = str(ROOT / "scraper")
if SCRAPER_DIR not in sys.path:
    sys.path.insert(0, SCRAPER_DIR)

import scrapers  # noqa: E402  (requires scraper/ on sys.path)
from scrapers import _util  # noqa: E402
from scrapers.base_scraper import BaseScraper  # noqa: E402

PORTED = {"gezat", "jiji", "mekina", "afromekina", "asiautos", "evprotec", "nbe", "nhtsa"}


# ---------------------------------------------------------------------------
# Registry wiring
# ---------------------------------------------------------------------------
def test_registry_contains_all_ported_scrapers():
    assert PORTED.issubset(set(scrapers.SCRAPER_REGISTRY))


def test_every_registry_entry_is_a_labelled_basescraper():
    for name, cls in scrapers.SCRAPER_REGISTRY.items():
        assert issubclass(cls, BaseScraper)
        assert cls.name == name
        assert isinstance(cls.base_url, str) and cls.base_url.startswith("http")


def test_get_scraper_rejects_unknown_names():
    with pytest.raises(ValueError):
        scrapers.get_scraper("does-not-exist")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def test_dig_reads_nested_keys_and_returns_none_on_miss():
    payload = {"a": {"b": {"c": 7}}}
    assert _util.dig(payload, "a", "b", "c") == 7
    assert _util.dig(payload, "a", "missing") is None
    assert _util.dig(None, "a") is None


def test_contact_details_are_redacted():
    text = "Call 0912 345 678 or email seller@example.com"
    clean = _util.remove_contact_details(text)
    assert "[phone removed]" in clean
    assert "[email removed]" in clean
    assert _util.remove_contact_details(None) is None


# ---------------------------------------------------------------------------
# Per-source parsing
# ---------------------------------------------------------------------------
def test_gezat_card_parsing():
    html = """
    <a class="gl-card" href="/listings/12345">
      <div>1,500,000</div><div>ETB</div><div>2022</div><div>BYD</div><div>Seagull</div>
      <div>12,000 km · Electric · Automatic</div><div>Addis Ababa</div><div>View details</div>
    </a>
    """
    card = BeautifulSoup(html, "html.parser").select_one("a.gl-card")
    row = scrapers.GezatSpider.card_to_row(card)
    assert row["listing_id"] == "12345"
    assert row["listing_url"] == "https://gezat.et/listings/12345"
    assert row["make"] == "BYD" and row["model"] == "Seagull"
    assert row["fuel_type"] == "Electric" and row["transmission"] == "Automatic"
    assert row["location"] == "Addis Ababa"


def test_jiji_advert_parsing_and_redaction():
    advert = {
        "id": 999,
        "url": "/ad/byd-seagull-1234",
        "title": "BYD Seagull — call 0912 345 678",
        "price_obj": {"value": 1500000},
        "price_title": "ETB 1,500,000",
        "schema_org": {"brand": {"name": "BYD"}, "model": "Seagull",
                       "vehicleModelDate": "2022", "fuelType": "Electric"},
        "attrs": [{"name": "Condition", "value": "Used"},
                  {"name": "Mileage", "value": "12000"}],
        "region_name": "Addis Ababa",
        "labels": [{"value": "Today"}],
    }
    row = scrapers.JijiSpider.advert_to_row(advert)
    assert row["listing_url"] == "https://jiji.com.et/ad/byd-seagull-1234"
    assert row["make"] == "BYD" and row["model"] == "Seagull"
    assert row["mileage_km"] == "12000" and row["price_value"] == 1500000
    assert "[phone removed]" in row["title"]
    assert row["listing_age_label"] == "Today"


def test_mekina_parsing_and_privacy_scrub():
    data = {"vehicles": [{"permalink": "byd-seagull-abc", "car": {"attributes": {
        "displayId": "MK-1", "title": "BYD Seagull 2022", "location": "Addis Ababa",
        "price": {"price": 1500000, "currency": "ETB"},
        "car_ch": {"year_made": 2022, "fuel": "Electric", "mileage": 12000,
                   "brand": {"data": {"attributes": {"name": "BYD"}}},
                   "model": {"data": {"attributes": {"name": "Seagull"}}}},
        "seller": {"name": "Real Seller", "phone": "0912345678", "social_media": "x"},
    }}}]}

    scrubbed = scrapers.MekinaSpider.remove_personal_data(data)
    seller = scrubbed["vehicles"][0]["car"]["attributes"]["seller"]
    assert seller["name"] == "[removed]" and seller["phone"] == "[removed]"

    row = scrapers.MekinaSpider.vehicle_to_row(data["vehicles"][0])
    assert row["listing_id"] == "MK-1"
    assert row["listing_url"] == "https://www.mekina.net/cars/byd-seagull-abc"
    assert row["make"] == "BYD" and row["model"] == "Seagull"
    assert row["price_value"] == 1500000 and row["currency"] == "ETB"


def test_afromekina_listing_row_and_url():
    listing = {"id": 13709, "brand": "changan", "model": "q05", "year": 2026,
               "title": "Changan Q05 2026", "price": 2500000, "currency": "ETB",
               "dealership": {"id": 1, "name": "Acme Motors"}}
    row = scrapers.AfroMekinaSpider.listing_to_row(listing)
    assert row["listing_url"] == "https://afromekina.com/cars/changan-q05-2026-13709"
    assert row["make"] == "changan" and row["dealership_name"] == "Acme Motors"


def test_afromekina_scrubs_dealership_payload():
    data = {"data": {"listings": [{"id": 1, "user": "bob", "phone": "0912345678",
                                   "dealership": {"id": 9, "name": "D", "extra": "drop-me"}}]}}
    scrubbed = scrapers.AfroMekinaSpider.remove_personal_data(data)["data"]["listings"][0]
    assert scrubbed["user"] == "[removed]" and scrubbed["phone"] == "[removed]"
    assert scrubbed["dealership"] == {"id": 9, "name": "D"}


def test_asiautos_product_row():
    product = {"id": 1, "title": "BYD Yuan Up Brake Pads", "product_type": "Brake Pads",
               "tags": ["byd", "brake"], "handle": "byd-yuan-up-brake-pads",
               "variants": [{"price": "29.99", "available": True}]}
    row = scrapers.AsiautosSpider.product_to_row(product)
    assert row["product_url"] == "https://asiautos.net/products/byd-yuan-up-brake-pads"
    assert row["tags"] == "byd, brake" and row["price"] == "29.99"


def test_evprotec_minor_unit_price_conversion():
    product = {"id": 7, "sku": "VW-ID4-001", "name": "ID.4 Headlight",
               "prices": {"price": "12999", "currency_minor_unit": 2, "currency_code": "AED"},
               "is_in_stock": True, "stock_availability": {"text": "In stock"},
               "permalink": "https://evprotec.com/p/x"}
    row = scrapers.EvprotecSpider.product_to_row(product, "vw-id4")
    assert row["price"] == pytest.approx(129.99)
    assert row["currency"] == "AED" and row["category"] == "vw-id4"


def test_nbe_rate_rows():
    payload = {"data": [{"date": "2024-05-01",
                         "currency": {"code": "USD", "name": "US Dollar"},
                         "buying": "56.1", "selling": "57.2", "weighted_average": "56.65"}]}
    rows = scrapers.NbeRatesSpider.rate_rows(payload)
    assert len(rows) == 1
    assert rows[0]["currency"] == "USD" and rows[0]["currency_name"] == "US Dollar"
    assert rows[0]["selling_etb"] == "57.2"
    assert scrapers.NbeRatesSpider.rate_rows(None) == []


def test_nhtsa_complaint_and_recall_rows_share_one_schema():
    complaint = scrapers.NhtsaSpider.complaint_row("TOYOTA", "BZ4X", 2024, {
        "odiNumber": 123, "dateComplaintFiled": "2024-01-01",
        "components": "ELECTRICAL SYSTEM", "summary": "Call 0912 345 678",
        "crash": False, "fire": False})
    recall = scrapers.NhtsaSpider.recall_row("VOLKSWAGEN", "ID.4", 2023, {
        "NHTSACampaignNumber": "24V-123", "ReportReceivedDate": "2024-02-01",
        "Component": "SUSPENSION", "Summary": "Bolt may loosen"})

    assert set(complaint) == set(scrapers.NhtsaSpider.FIELDNAMES)
    assert set(recall) == set(scrapers.NhtsaSpider.FIELDNAMES)
    assert complaint["record_type"] == "complaint" and complaint["ref_number"] == 123
    assert "[phone removed]" in complaint["summary"]
    assert recall["record_type"] == "recall" and recall["ref_number"] == "24V-123"
    assert recall["component"] == "SUSPENSION"
