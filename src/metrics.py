import sqlite3
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "transactions.db"


def _filters(user_id: Optional[str] = None, month: Optional[int] = None, year: Optional[int] = None) -> tuple:
    conditions = []
    params = []

    if user_id:
        conditions.append("user_id = ?")
        params.append(user_id)
    if month:
        conditions.append("month = ?")
        params.append(month)
    if year:
        conditions.append("year = ?")
        params.append(year)

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, params


def get_global_summary(user_id=None, month=None, year=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    where, params = _filters(user_id, month, year)

    cur.execute(f"""
        SELECT
          COUNT(*) as total_transactions,
          ROUND(SUM(CASE WHEN transaction_type='debit' THEN amount ELSE 0 END), 2) as total_spend,
          ROUND(SUM(CASE WHEN transaction_type='credit' THEN amount ELSE 0 END), 2) as total_income,
          ROUND(AVG(CASE WHEN transaction_type='debit' THEN amount ELSE NULL END), 2) as avg_transaction
        FROM transactions {where}
    """, params)

    row = cur.fetchone()
    conn.close()
    return {
        "total_transactions": row[0],
        "total_spend": row[1] or 0,
        "total_income": row[2] or 0,
        "avg_transaction": row[3] or 0,
        "net": round((row[2] or 0) - (row[1] or 0), 2),
    }


def get_spend_by_category(user_id=None, month=None, year=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    where, params = _filters(user_id, month, year)
    if where:
        where += " AND transaction_type = 'debit'"
    else:
        where = "WHERE transaction_type = 'debit'"

    cur.execute(f"""
        SELECT merchant_category,
               COUNT(*) as count,
               ROUND(SUM(amount), 2) as total_spend
        FROM transactions {where}
        GROUP BY merchant_category
        ORDER BY total_spend DESC
    """, params)

    rows = [{"category": r[0], "count": r[1], "total_spend": r[2]} for r in cur.fetchall()]
    conn.close()
    return rows


def get_top_merchants(user_id=None, month=None, year=None, limit=5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    where, params = _filters(user_id, month, year)
    if where:
        where += " AND transaction_type = 'debit'"
    else:
        where = "WHERE transaction_type = 'debit'"

    cur.execute(f"""
        SELECT merchant_name,
               COUNT(*) as count,
               ROUND(SUM(amount), 2) as total_spend
        FROM transactions {where}
        GROUP BY merchant_name
        ORDER BY total_spend DESC
        LIMIT {limit}
    """, params)

    rows = [{"merchant": r[0], "count": r[1], "total_spend": r[2]} for r in cur.fetchall()]
    conn.close()
    return rows


def get_recurring_spend(user_id=None, month=None, year=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    where, params = _filters(user_id, month, year)
    if where:
        where += " AND is_recurring = 1"
    else:
        where = "WHERE is_recurring = 1"

    cur.execute(f"""
        SELECT ROUND(SUM(amount), 2) as recurring_spend,
               COUNT(*) as recurring_count
        FROM transactions {where}
    """, params)

    row = cur.fetchone()
    conn.close()
    return {"recurring_spend": row[0] or 0, "recurring_count": row[1] or 0}


def get_anomalies(user_id=None, month=None, year=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    where, params = _filters(user_id, month, year)
    if where:
        where += " AND is_anomaly = 1"
    else:
        where = "WHERE is_anomaly = 1"

    cur.execute(f"""
        SELECT id, date, merchant_name, merchant_category, amount
        FROM transactions {where}
        ORDER BY amount DESC
    """, params)

    rows = [{"id": r[0], "date": r[1], "merchant": r[2], "category": r[3], "amount": r[4]} for r in cur.fetchall()]
    conn.close()
    return rows