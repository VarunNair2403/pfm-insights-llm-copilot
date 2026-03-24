import sys
from .metrics import (
    get_global_summary,
    get_spend_by_category,
    get_top_merchants,
    get_recurring_spend,
    get_anomalies,
)

def main():
    user_id = sys.argv[1] if len(sys.argv) > 1 else None
    month = int(sys.argv[2]) if len(sys.argv) > 2 else None
    year = int(sys.argv[3]) if len(sys.argv) > 3 else None

    print("SUMMARY:", get_global_summary(user_id, month, year))
    print("BY CATEGORY:", get_spend_by_category(user_id, month, year))
    print("TOP MERCHANTS:", get_top_merchants(user_id, month, year))
    print("RECURRING:", get_recurring_spend(user_id, month, year))
    print("ANOMALIES:", get_anomalies(user_id, month, year))

if __name__ == "__main__":
    main()