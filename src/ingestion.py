import sqlite3
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "transactions.db"
CSV_PATH = DATA_DIR / "transactions_raw.csv"

DDL = """
CREATE TABLE IF NOT EXISTS transactions (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  amount REAL NOT NULL,
  currency TEXT NOT NULL,
  merchant_name TEXT NOT NULL,
  merchant_category TEXT NOT NULL,
  transaction_type TEXT NOT NULL,
  account_type TEXT NOT NULL,
  user_id TEXT NOT NULL,
  month INTEGER NOT NULL,
  year INTEGER NOT NULL,
  is_recurring INTEGER NOT NULL,
  is_anomaly INTEGER NOT NULL
);
"""


def load_csv_to_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(DDL)

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                r["id"], r["date"], float(r["amount"]), r["currency"],
                r["merchant_name"], r["merchant_category"], r["transaction_type"],
                r["account_type"], r["user_id"], int(r["month"]), int(r["year"]),
                int(r["is_recurring"]), int(r["is_anomaly"])
            )
            for r in reader
        ]
        cur.executemany(
            """
            INSERT OR REPLACE INTO transactions VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            rows
        )

    conn.commit()
    conn.close()
    print(f"Loaded {len(rows)} rows into transactions.db")


if __name__ == "__main__":
    load_csv_to_db()