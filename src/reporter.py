from typing import Dict, Optional
from .llm_client import generate_insights


def build_prompt(snapshot: Dict) -> str:
    summary = snapshot["summary"]
    categories = snapshot["by_category"]
    merchants = snapshot["top_merchants"]
    recurring = snapshot["recurring"]
    anomalies = snapshot["anomalies"]

    category_lines = "\n".join(
        f"  {c['category']}: ${c['total_spend']:,.2f} ({c['count']} transactions)"
        for c in categories
    )

    merchant_lines = "\n".join(
        f"  {m['merchant']}: ${m['total_spend']:,.2f} ({m['count']} transactions)"
        for m in merchants
    )

    anomaly_lines = "\n".join(
        f"  {a['merchant']} on {a['date']}: ${a['amount']:,.2f} (category: {a['category']})"
        for a in anomalies
    ) or "  None detected"

    return (
        "You are a personal finance advisor.\n"
        "Based on the spending data below, write a friendly 4-5 sentence monthly financial insight.\n"
        "Cover: overall financial health, biggest spending category, any unusual transactions, "
        "and one specific actionable nudge the user can act on this month.\n\n"
        f"=== Monthly Summary ===\n"
        f"Total transactions: {summary['total_transactions']}\n"
        f"Total spend: ${summary['total_spend']:,.2f}\n"
        f"Total income: ${summary['total_income']:,.2f}\n"
        f"Net: ${summary['net']:,.2f}\n"
        f"Avg transaction: ${summary['avg_transaction']:,.2f}\n\n"
        f"=== Spend by Category ===\n{category_lines}\n\n"
        f"=== Top Merchants ===\n{merchant_lines}\n\n"
        f"=== Recurring Spend ===\n"
        f"  Total: ${recurring['recurring_spend']:,.2f} across {recurring['recurring_count']} transactions\n\n"
        f"=== Anomalies ===\n{anomaly_lines}\n"
    )


def generate_narrative(snapshot: Dict) -> str:
    prompt = build_prompt(snapshot)
    return generate_insights(prompt)