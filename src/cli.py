import sys
from .metrics import (
    get_global_summary,
    get_spend_by_category,
    get_top_merchants,
    get_recurring_spend,
    get_anomalies,
)
from .reporter import generate_narrative


def main():
    user_id = sys.argv[1] if len(sys.argv) > 1 else None
    month = int(sys.argv[2]) if len(sys.argv) > 2 else None
    year = int(sys.argv[3]) if len(sys.argv) > 3 else None

    snapshot = {
        "user_id": user_id or "all_users",
        "month": month,
        "year": year,
        "summary": get_global_summary(user_id, month, year),
        "by_category": get_spend_by_category(user_id, month, year),
        "top_merchants": get_top_merchants(user_id, month, year),
        "recurring": get_recurring_spend(user_id, month, year),
        "anomalies": get_anomalies(user_id, month, year),
    }

    narrative = generate_narrative(snapshot)

    print("SNAPSHOT:", snapshot)
    print("\nINSIGHTS:")
    print(narrative)


if __name__ == "__main__":
    main()