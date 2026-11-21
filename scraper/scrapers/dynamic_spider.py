import time
from typing import Any, Dict, List
from .base_scraper import BaseScraper

class DynamicScraper(BaseScraper):
    """
    Template for scraping modern JavaScript-rendered websites using Playwright.
    Falls back gracefully if playwright is not installed.
    """

    name = "dynamic_sample"
    base_url = "https://quotes.toscrape.com/js/"

    def scrape(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[Warning] 'playwright' is not installed or available. Run 'pip install playwright && playwright install'")
            return []

        results = []
        with sync_playwright() as p:
            # Launch headless browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = context.new_page()

            page.goto(self.base_url, timeout=30000)
            # Wait for dynamic JS content to mount
            page.wait_for_selector(".quote", timeout=10000)

            quotes = page.query_selector_all(".quote")
            for q in quotes:
                text_elem = q.query_selector(".text")
                author_elem = q.query_selector(".author")
                tag_elems = q.query_selector_all(".tags .tag")

                results.append({
                    "quote": text_elem.inner_text().strip() if text_elem else "",
                    "author": author_elem.inner_text().strip() if author_elem else "",
                    "tags": [t.inner_text().strip() for t in tag_elems],
                    "rendered_with": "playwright",
                })

            browser.close()

        return results
