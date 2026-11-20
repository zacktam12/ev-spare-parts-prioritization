from typing import Dict, Type
from .base_scraper import BaseScraper
from .quotes_spider import QuotesScraper
from .books_spider import BooksScraper
from .dynamic_spider import DynamicScraper
from .landin_spider import LandinSpider
from .adey_spider import AdeyMarketSpider

# Central registry of available scrapers
SCRAPER_REGISTRY: Dict[str, Type[BaseScraper]] = {
    QuotesScraper.name: QuotesScraper,
    BooksScraper.name: BooksScraper,
    DynamicScraper.name: DynamicScraper,
    LandinSpider.name: LandinSpider,
    AdeyMarketSpider.name: AdeyMarketSpider,
}

def get_scraper(name: str) -> Type[BaseScraper]:
    if name not in SCRAPER_REGISTRY:
        raise ValueError(f"Unknown scraper '{name}'. Available: {list(SCRAPER_REGISTRY.keys())}")
    return SCRAPER_REGISTRY[name]

__all__ = [
    "SCRAPER_REGISTRY",
    "get_scraper",
    "BaseScraper",
    "QuotesScraper",
    "BooksScraper",
    "DynamicScraper",
    "LandinSpider",
    "AdeyMarketSpider",
]
