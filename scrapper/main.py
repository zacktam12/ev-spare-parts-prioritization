import argparse
import sys
from pathlib import Path
from scrapers import SCRAPER_REGISTRY, get_scraper
from storage import DataExporter

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-Source Web Scraper CLI")
    parser.add_argument(
        "--scraper", "-s",
        type=str,
        help="Name of the specific scraper to run (e.g. quotes, books, dynamic_sample)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all registered scrapers"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available scrapers"
    )
    parser.add_argument(
        "--pages", "-p",
        type=int,
        default=2,
        help="Maximum pages to scrape per website (default: 2)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "csv", "sqlite"],
        default="json",
        help="Output data format: json, csv, or sqlite (default: json)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Custom output file path. Defaults to outputs/<scraper_name>.<ext>"
    )
    return parser.parse_args()

def save_scraped_data(name: str, data: list, output_format: str, custom_path: str = None):
    ext_map = {"json": ".json", "csv": ".csv", "sqlite": ".db"}
    if custom_path:
        out_path = Path(custom_path)
    else:
        out_path = Path("outputs") / f"{name}{ext_map[output_format]}"

    if output_format == "json":
        saved_file = DataExporter.to_json(data, out_path)
    elif output_format == "csv":
        saved_file = DataExporter.to_csv(data, out_path)
    elif output_format == "sqlite":
        saved_file = DataExporter.to_sqlite(data, out_path, table_name=name)

    print(f"  [+] Saved {len(data)} items to: {saved_file}")

def run_single(name: str, pages: int, output_format: str, output_path: str = None):
    print(f"\n[*] Starting scraper: '{name}' (Max pages: {pages})")
    scraper_cls = get_scraper(name)
    with scraper_cls() as scraper:
        data = scraper.scrape(max_pages=pages)
        print(f"[*] Scraped {len(data)} items from '{name}'")
        if data:
            save_scraped_data(name, data, output_format, output_path)
        else:
            print(f"[-] No items collected for '{name}'")

def main():
    args = parse_args()

    if args.list:
        print("\nAvailable scrapers:")
        for name, cls in SCRAPER_REGISTRY.items():
            doc = (cls.__doc__ or "No description").strip().split("\n")[0]
            print(f" - {name:<16} : {doc}")
        sys.exit(0)

    if args.all:
        for name in SCRAPER_REGISTRY:
            try:
                run_single(name, args.pages, args.format)
            except Exception as e:
                print(f"[!] Error running {name}: {e}")
        print("\n[✔] Finished running all scrapers.")
        sys.exit(0)

    if args.scraper:
        try:
            run_single(args.scraper, args.pages, args.format, args.output)
        except Exception as e:
            print(f"[!] Error: {e}")
            sys.exit(1)
        sys.exit(0)

    print("Please specify a scraper with --scraper <name>, --all to run all, or --list to see available scrapers.")

if __name__ == "__main__":
    main()
