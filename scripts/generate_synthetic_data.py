import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CSV_PATH = DATA_DIR / "transactions_raw.csv"

# --- Config ---
NUM_ROWS = 500
START_DATE = datetime(2025, 10, 1)
END_DATE = datetime(2026, 3, 22)
USER_IDS = ["user_001", "user_002", "user_003"]

# --- Reference Data ---
CATEGORIES = {
    "food_and_drink": ["Starbucks", "Chipotle", "McDonalds", "Dunkin", "Sweetgreen", "Shake Shack"],
    "groceries": ["Whole Foods", "Trader Joes", "Walmart Grocery", "Costco", "Stop and Shop"],
    "transport": ["Uber", "Lyft", "NJ Transit", "MTA", "Citi Bike", "EZPass"],
    "subscriptions": ["Netflix", "Spotify", "Apple One", "ChatGPT Plus", "Amazon Prime", "Hulu"],
    "shopping": ["Amazon", "Target", "Zara", "H&M", "Nike", "Best Buy"],
    "utilities": ["PSE&G", "Verizon", "Comcast", "Con Edison"],
    "health": ["CVS", "Walgreens", "Gym Membership", "Doctor Visit", "Dental"],
    "travel": ["Delta Airlines", "Airbnb", "Marriott", "United Airlines", "Booking.com"],
    "rent": ["Rent Payment"],
    "income": ["Payroll Direct Deposit", "Freelance Payment", "Tax Refund"],
}

AMOUNT_RANGES = {
    "food_and_drink": (5, 60),
    "groceries": (30, 200),
    "transport": (3, 80),
    "subscriptions": (10, 25),
    "shopping": (20, 300),
    "utilities": (50, 200),
    "health": (10, 250),
    "travel": (100, 1200),
    "rent": (1800, 2200),
    "income": (3000, 6000),
}

FIELDNAMES = [
    "id", "date", "amount", "currency", "merchant_name", "merchant_category",
    "transaction_type", "account_type", "user_id", "month", "year",
    "is_recurring", "is_anomaly"
]


def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def generate_row():
    category = random.choices(
        list(CATEGORIES.keys()),
        weights=[20, 10, 10, 8, 10, 5, 5, 3, 2, 7],
        k=1
    )[0]

    merchant = random.choice(CATEGORIES[category])
    low, high = AMOUNT_RANGES[category]
    amount = round(random.uniform(low, high), 2)

    transaction_type = "credit" if category == "income" else "debit"
    account_type = random.choice(["checking", "credit_card"])
    is_recurring = 1 if category in ["subscriptions", "rent", "utilities"] else 0

    # inject a few anomalies
    is_anomaly = 0
    if category in ["shopping", "travel"] and random.random() < 0.05:
        amount = round(amount * random.uniform(3, 5), 2)
        is_anomaly = 1

    date = random_date(START_DATE, END_DATE)

    return {
        "id": "txn_" + uuid.uuid4().hex[:10],
        "date": date.strftime("%Y-%m-%d"),
        "amount": amount,
        "currency": "usd",
        "merchant_name": merchant,
        "merchant_category": category,
        "transaction_type": transaction_type,
        "account_type": account_type,
        "user_id": random.choice(USER_IDS),
        "month": date.month,
        "year": date.year,
        "is_recurring": is_recurring,
        "is_anomaly": is_anomaly,
    }


if __name__ == "__main__":
    rows = [generate_row() for _ in range(NUM_ROWS)]
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {NUM_ROWS} rows → {CSV_PATH}")