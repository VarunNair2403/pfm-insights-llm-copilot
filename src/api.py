from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime

from .metrics import (
    get_global_summary,
    get_spend_by_category,
    get_top_merchants,
    get_recurring_spend,
    get_anomalies,
)
from .reporter import generate_narrative

app = FastAPI(
    title="PFM Insights — LLM Copilot",
    description="AI-powered personal finance insights API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/summary")
def get_summary(
    user_id: Optional[str] = Query(None),
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
):
    return {
        "user_id": user_id or "all_users",
        "month": month,
        "year": year,
        "summary": get_global_summary(user_id, month, year),
        "by_category": get_spend_by_category(user_id, month, year),
        "top_merchants": get_top_merchants(user_id, month, year),
        "recurring": get_recurring_spend(user_id, month, year),
        "anomalies": get_anomalies(user_id, month, year),
    }


@app.get("/anomalies")
def get_anomaly_list(
    user_id: Optional[str] = Query(None),
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
):
    anomalies = get_anomalies(user_id, month, year)
    return {
        "user_id": user_id or "all_users",
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
    }


@app.get("/insights")
def get_insights(
    user_id: Optional[str] = Query(None),
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
):
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
    return {
        "snapshot": snapshot,
        "narrative": narrative,
    }