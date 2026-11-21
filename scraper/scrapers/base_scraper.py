import time
import httpx
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from config import config

class BaseScraper(ABC):
    """Abstract base class for all individual scrapers."""
    
    name: str = "base"
    base_url: str = ""

    def __init__(self, delay: Optional[float] = None, timeout: Optional[float] = None):
        self.delay = delay if delay is not None else config.delay_between_requests
        self.timeout = timeout if timeout is not None else config.timeout
        self.client = httpx.Client(
            headers=config.random_headers,
            timeout=self.timeout,
            verify=config.verify_ssl,
            follow_redirects=True,
        )

    def fetch_html(self, url: str, params: Optional[Dict[str, Any]] = None, retries: int = config.max_retries) -> str:
        """Fetches raw HTML string from a given URL with automatic retries."""
        for attempt in range(1, retries + 1):
            try:
                response = self.client.get(url, params=params, headers=config.random_headers)
                response.raise_for_status()
                if self.delay > 0:
                    time.sleep(self.delay)
                return response.text
            except (httpx.HTTPError, httpx.RequestError) as err:
                if attempt == retries:
                    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts: {err}")
                time.sleep(attempt * 1.5)
        return ""

    def parse_soup(self, html: str) -> BeautifulSoup:
        """Parses HTML using BeautifulSoup."""
        return BeautifulSoup(html, "html.parser")

    @abstractmethod
    def scrape(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        """Main scraping routine to be implemented by each spider."""
        pass

    def close(self):
        """Close HTTP client connections."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
