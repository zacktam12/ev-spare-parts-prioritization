from typing import Dict, Type
from .base_scraper import BaseScraper
from .quotes_spider import QuotesScraper
from .books_spider import BooksScraper
from .dynamic_spider import DynamicScraper
from .landin_spider import LandinSpider
from .adey_spider import AdeyMarketSpider
from .gezat_spider import GezatSpider
from .jiji_spider import JijiSpider
from .mekina_spider import MekinaSpider
from .afromekina_spider import AfroMekinaSpider
from .asiautos_spider import AsiautosSpider
from .evprotec_spider import EvprotecSpider
from .nbe_spider import NbeRatesSpider
from .nhtsa_spider import NhtsaSpider

# Central registry of available scrapers
SCRAPER_REGISTRY: Dict[str, Type[BaseScraper]] = {
    QuotesScraper.name: QuotesScraper,
    BooksScraper.name: BooksScraper,
    DynamicScraper.name: DynamicScraper,
    LandinSpider.name: LandinSpider,
    AdeyMarketSpider.name: AdeyMarketSpider,
    # Ethiopian marketplace listings
    GezatSpider.name: GezatSpider,
    JijiSpider.name: JijiSpider,
    MekinaSpider.name: MekinaSpider,
    AfroMekinaSpider.name: AfroMekinaSpider,
    # Parts suppliers & reference data
    AsiautosSpider.name: AsiautosSpider,
    EvprotecSpider.name: EvprotecSpider,
    NbeRatesSpider.name: NbeRatesSpider,
    NhtsaSpider.name: NhtsaSpider,
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
    "GezatSpider",
    "JijiSpider",
    "MekinaSpider",
    "AfroMekinaSpider",
    "AsiautosSpider",
    "EvprotecSpider",
    "NbeRatesSpider",
    "NhtsaSpider",
]
