"""Shared helpers for the ported (formerly ev3) collectors.

These utilities centralise the small pieces of behaviour the ported spiders have in
common: safe nested-JSON reads, UTC timestamps, contact-detail redaction, and a
robots.txt-respecting fetch wrapper.
"""

import json
import re
import urllib.robotparser
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

import httpx

# Stable identifier used when consulting robots.txt.
USER_AGENT = "ev-parts-research/1.0 (internship project)"
ROBOTS_TIMEOUT = 15.0

_robots_cache: dict = {}


def now_utc() -> str:
    """Current UTC timestamp, second precision (matches the ev3 collector format)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def dig(data: Any, *keys: str) -> Any:
    """Read nested JSON safely: dig(car, "price", "value") -> value or None."""
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?251[\s-]?|0)[79](?:[\s-]?\d){8}(?!\d)")
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def remove_contact_details(text: Any) -> Any:
    """Redact phone numbers and e-mail addresses (listings are published openly)."""
    if not isinstance(text, str):
        return text
    text = PHONE_PATTERN.sub("[phone removed]", text)
    text = EMAIL_PATTERN.sub("[email removed]", text)
    return text


def _robots_for(url: str) -> urllib.robotparser.RobotFileParser:
    parts = urlparse(url)
    site = f"{parts.scheme}://{parts.netloc}"

    if site not in _robots_cache:
        parser = urllib.robotparser.RobotFileParser()
        try:
            response = httpx.get(site + "/robots.txt", timeout=ROBOTS_TIMEOUT,
                                 follow_redirects=True)
            parser.parse(response.text.splitlines() if response.status_code == 200 else [])
        except httpx.HTTPError:
            parser.parse([])
        _robots_cache[site] = parser

    return _robots_cache[site]


def is_allowed_by_robots(url: str) -> bool:
    """Whether robots.txt permits fetching ``url`` with our User-Agent."""
    try:
        return _robots_for(url).can_fetch(USER_AGENT, url)
    except Exception:  # pragma: no cover - defensive: never block on a malformed robots.txt
        return True


def guarded_get(scraper, url: str, params: Optional[dict] = None) -> Optional[str]:
    """Fetch text through a BaseScraper instance, honouring robots.txt.

    Returns the response body as text, or ``None`` when the fetch is disallowed or
    fails after retries (so callers can simply break out of a pagination loop).
    """
    if not is_allowed_by_robots(url):
        return None
    try:
        return scraper.fetch_html(url, params=params)
    except RuntimeError:
        return None


def guarded_get_json(scraper, url: str, params: Optional[dict] = None) -> Any:
    """Like :func:`guarded_get` but parses the body as JSON (``None`` on failure)."""
    text = guarded_get(scraper, url, params=params)
    if text is None:
        return None
    try:
        return json.loads(text)
    except ValueError:
        return None
