import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Union

class DataExporter:
    """Exports structured scraping results to JSON, CSV, or SQLite."""

    @staticmethod
    def ensure_output_dir(filepath: Union[str, Path]) -> Path:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def to_json(cls, data: List[Dict[str, Any]], filepath: Union[str, Path], indent: int = 2) -> Path:
        path = cls.ensure_output_dir(filepath)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return path

    @classmethod
    def to_csv(cls, data: List[Dict[str, Any]], filepath: Union[str, Path]) -> Path:
        path = cls.ensure_output_dir(filepath)
        if not data:
            with open(path, "w", encoding="utf-8", newline="") as f:
                pass
            return path

        keys = list(data[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in data:
                # Convert list or complex dict values into json string for CSV cells
                formatted_row = {
                    k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
                    for k, v in row.items()
                }
                writer.writerow(formatted_row)
        return path

    @classmethod
    def to_sqlite(cls, data: List[Dict[str, Any]], db_path: Union[str, Path], table_name: str = "scraped_data") -> Path:
        path = cls.ensure_output_dir(db_path)
        if not data:
            return path

        keys = list(data[0].keys())
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # Create table with dynamic columns
        columns_sql = ", ".join([f'"{k}" TEXT' for k in keys])
        cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_sql})')

        placeholders = ", ".join(["?"] * len(keys))
        columns_str = ", ".join([f'"{k}"' for k in keys])
        sql = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'

        rows = []
        for row in data:
            rows.append(tuple(
                (json.dumps(row.get(k), ensure_ascii=False) if isinstance(row.get(k), (list, dict)) else str(row.get(k, "")))
                for k in keys
            ))

        cursor.executemany(sql, rows)
        conn.commit()
        conn.close()
        return path
