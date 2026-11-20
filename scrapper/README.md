# Universal Multi-Source Web Scraper

A modular, extensible Python web scraper capable of extracting data from multiple websites using static HTML parsing (`BeautifulSoup` + `httpx`), browser automation (`Playwright`) for JavaScript-heavy/dynamic sites, and saving results into formats like **JSON**, **CSV**, or **SQLite**.

---

## 🚀 Key Features

1. **Modular Spider Architecture**: Plug-and-play scrapers for each target website under `scrapers/`.
2. **Dual Engine Support**:
   - **Fast HTTP engine** (`httpx` + `BeautifulSoup4`) for standard static and SSR pages with custom headers, retries, and User-Agent rotation.
   - **Dynamic browser engine** (`Playwright`) for single-page apps (SPAs), infinite scroll, or client-heavy content.
3. **Multiple Export Formats**: Automatically export scraped data to JSON, CSV, or SQLite.
4. **Command-Line Interface (CLI)**: Run individual site scrapers or all scrapers with configurable outputs.
5. **Configurable Settings**: User-agent rotation, request timeouts, concurrency/rate-limiting to scrape politely.
6. **Domain Scrapers**:
   - **Landin Parts (`landin`)**: Built for EV Spare-Parts Import Prioritization (BYD Seagull spare-parts catalog).
   - **Adey Market (`adey`)**: Built for Ethiopian EV marketplace listing intelligence covering the 5 candidate EV models.

---

## 📁 Project Structure

```text
scrapper/
│── config.py            # Global settings (headers, timeouts, rate limits)
│── main.py              # CLI entry point to run scrapers
│── requirements.txt     # Python dependencies
│── scrapers/
│   │── __init__.py      # Package export and central registry
│   │── base_scraper.py  # Abstract base scraper class
│   │── landin_spider.py # BYD Seagull scraper for Landin Parts catalog
│   │── adey_spider.py   # Ethiopian EV marketplace scraper for Adey Market
│   │── quotes_spider.py # Sample scraper for static site (quotes.toscrape.com)
│   │── books_spider.py  # Sample scraper for pagination (books.toscrape.com)
│   └── dynamic_spider.py# Sample scraper for dynamic/JS content
│── storage/
│   │── __init__.py
│   └── exporter.py      # Data exporter (JSON, CSV, SQLite)
└── outputs/             # Output folder for generated files
    ├── adey_raw.csv     # Raw unfiltered Adey Market EV listings
    ├── adey_raw.json    # Raw unfiltered Adey Market EV listings (JSON)
    ├── adey_cleaned.csv # Cleaned & normalized candidate EV listings
    ├── adey_cleaned.json# Cleaned & normalized candidate EV listings (JSON)
    ├── landin.csv       # Baseline raw BYD Seagull parts (CSV)
    ├── landin_verified.csv # 35 verified unique part applications
    ├── landin_review.csv   # 150 review & conflict items
    └── landin_quality_audit.md # Quality audit report
```

---

## 🛠️ Quick Start

> New to the project? Start with [PROJECT_GUIDE_FOR_PRESENTATION.md](./PROJECT_GUIDE_FOR_PRESENTATION.md) for a beginner-friendly explanation of the code, data flow, scoring, limitations, and presentation language.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Optional: For dynamic JS sites using Playwright)*
```bash
playwright install chromium
```

### 2. Run Scrapers

- List all available scrapers:
  ```bash
  python main.py --list
  ```

- **Run Adey Market Scraper (Ethiopian EV Marketplace Listings)**:
  ```bash
  python main.py --scraper adey --format csv
  ```
  *Outputs:*
  - `outputs/adey_raw.csv` and `outputs/adey_raw.json`: Complete raw extracted listings across EV categories.
  - `outputs/adey_cleaned.csv` and `outputs/adey_cleaned.json`: Filtered and normalized dataset covering the 5 candidate vehicle models (*BYD Seagull, BYD Yuan Up, Changan Benben E-Star, Toyota bZ4X, Volkswagen ID.4 / ID.6*).

- **Run Landin Parts Scraper (BYD Seagull EV Parts)**:
  ```bash
  python main.py --scraper landin --format csv
  ```

- Run sample scrapers:
  ```bash
  python main.py --scraper quotes --format json
  python main.py --scraper books --format csv
  ```

- Run all scrapers:
  ```bash
  python main.py --all --format json
  ```
