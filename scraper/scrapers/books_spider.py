from urllib.parse import urljoin
from typing import Any, Dict, List
from .base_scraper import BaseScraper

class BooksScraper(BaseScraper):
    """Scrapes book titles, prices, ratings, and availability from books.toscrape.com."""

    name = "books"
    base_url = "https://books.toscrape.com/catalogue/page-1.html"

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def scrape(self, max_pages: int = 2) -> List[Dict[str, Any]]:
        results = []
        current_url = self.base_url
        page = 1

        while current_url and page <= max_pages:
            html = self.fetch_html(current_url)
            soup = self.parse_soup(html)

            articles = soup.select("article.product_pod")
            for article in articles:
                title_elem = article.select_one("h3 a")
                title = title_elem["title"] if title_elem and "title" in title_elem.attrs else (title_elem.text if title_elem else "")
                rel_link = title_elem["href"] if title_elem and "href" in title_elem.attrs else ""
                book_url = urljoin(current_url, rel_link)

                price_elem = article.select_one(".price_color")
                price = price_elem.get_text(strip=True) if price_elem else ""

                avail_elem = article.select_one(".availability")
                availability = avail_elem.get_text(strip=True) if avail_elem else ""

                rating_elem = article.select_one("p.star-rating")
                rating = 0
                if rating_elem:
                    classes = rating_elem.get("class", [])
                    for cls in classes:
                        if cls in self.RATING_MAP:
                            rating = self.RATING_MAP[cls]
                            break

                results.append({
                    "title": title,
                    "price": price,
                    "rating_stars": rating,
                    "availability": availability,
                    "url": book_url,
                })

            # Check next page link
            next_elem = soup.select_one("li.next a")
            if next_elem and "href" in next_elem.attrs:
                current_url = urljoin(current_url, next_elem["href"])
                page += 1
            else:
                break

        return results
