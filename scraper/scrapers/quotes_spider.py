from urllib.parse import urljoin
from typing import Any, Dict, List
from .base_scraper import BaseScraper

class QuotesScraper(BaseScraper):
    """Scrapes inspirational quotes, authors, and tags from quotes.toscrape.com."""

    name = "quotes"
    base_url = "https://quotes.toscrape.com"

    def scrape(self, max_pages: int = 2) -> List[Dict[str, Any]]:
        results = []
        current_url = self.base_url
        page = 1

        while current_url and page <= max_pages:
            html = self.fetch_html(current_url)
            soup = self.parse_soup(html)

            quote_elements = soup.select(".quote")
            for elem in quote_elements:
                text = elem.select_one(".text").get_text(strip=True) if elem.select_one(".text") else ""
                author = elem.select_one(".author").get_text(strip=True) if elem.select_one(".author") else ""
                tags = [t.get_text(strip=True) for t in elem.select(".tags .tag")]
                author_link = elem.select_one("span a")
                author_url = urljoin(self.base_url, author_link["href"]) if author_link else ""

                results.append({
                    "quote": text,
                    "author": author,
                    "tags": tags,
                    "author_profile": author_url,
                    "source_url": current_url,
                })

            # Pagination check
            next_btn = soup.select_one("li.next a")
            if next_btn and "href" in next_btn.attrs:
                current_url = urljoin(self.base_url, next_btn["href"])
                page += 1
            else:
                break

        return results
