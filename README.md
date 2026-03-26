# PFM Insights — LLM Copilot

## The Problem

Most people have access to their transaction data but get almost no insight from it. Banks show you a list of transactions. Some apps categorize them. But nobody tells you why your month was expensive, what changed compared to last month, and what you should actually do differently — in plain English.

Financial literacy tools today are either too simple (pie charts of spending) or too complex (spreadsheet-level budgeting). There is a gap between raw data and actionable guidance that most people never bridge.

This tool bridges that gap using AI.

---

## Why I Built This

I built this as a portfolio project to simulate the kind of AI-powered personal finance feature a company like Plaid, Apple Card, or a neobank would build internally. The goal was to combine:

- **Real PFM domain knowledge** — categories, recurring spend, anomaly detection, income vs spend tracking
- **LLM-powered narrative generation** — instead of numbers, get a friendly 4-5 sentence monthly summary with a specific nudge
- **Anomaly detection** — automatically flag transactions that look unusual based on amount and category
- **Production-ready API** — FastAPI layer so this could power a mobile app, Slack bot, or internal dashboard

This project demonstrates how AI can turn raw financial data into something a real user would find genuinely useful.

---

## How It Works

1. transactions_raw.csv is loaded into a SQLite database via ingestion.py
2. metrics.py computes spending KPIs globally and broken down by category, merchant, and recurring vs one-time
3. anomalies are flagged during data generation and surfaced via the anomalies endpoint
4. reporter.py builds a structured prompt from all KPIs and sends it to GPT-4o-mini
5. cli.py or api.py delivers the output — either via terminal or REST API

---

## Project Structure and File Explanations

**data/transactions_raw.csv** — Raw transaction data (synthetic, 500 rows spanning Oct 2025 to Mar 2026). In production this would come from a Plaid API connection or a bank data feed.

**scripts/generate_synthetic_data.py** — Generates 500 realistic personal finance transactions across categories including food, rent, groceries, transport, subscriptions, shopping, health, travel, and income. Injects a small number of anomalies to simulate unusual spending spikes.

**src/ingestion.py** — Loads the CSV into a local SQLite database. Simulates an ETL step; in production this would be a scheduled pipeline pulling from a transactional database or data warehouse.

**src/metrics.py** — Computes all KPIs with optional filtering by user, month, and year. Covers global summary, spend by category, top merchants, recurring spend, and anomaly retrieval.

**src/reporter.py** — Builds a structured LLM prompt from the snapshot data and calls the OpenAI client. Prompt is designed to produce a friendly, user-facing narrative with a concrete actionable nudge.

**src/llm_client.py** — OpenAI API wrapper. Isolated so you can swap GPT for Claude, Gemini, or an internal model without touching any other file.

**src/cli.py** — CLI entrypoint. Accepts user_id, month, and year as arguments. Prints full snapshot and LLM narrative to terminal.

**src/api.py** — FastAPI REST API with four endpoints covering health, summary, anomalies, and full insights with narrative.

---

## Quickstart (Local)

**1. Clone and set up environment**

```bash
git clone https://github.com/VarunNair2403/pfm-insights-llm-copilot.git
cd pfm-insights-llm-copilot
python -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv fastapi uvicorn
```

**2. Add your OpenAI key**

Create a .env file in the project root:

```env
OPENAI_API_KEY=sk-...
```

**3. Generate data and load DB**

```bash
python scripts/generate_synthetic_data.py
python -m src.ingestion
```

**4. Run via CLI**

```bash
python -m src.cli                        # all users, all time
python -m src.cli user_001               # specific user, all time
python -m src.cli user_001 3 2026        # specific user, March 2026
```

**5. Run via API**

```bash
uvicorn src.api:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive Swagger UI.

---

## API Endpoints

- GET /health — Service liveness check
- GET /summary?user_id=user_001&month=3&year=2026 — Raw KPIs with category and merchant breakdowns
- GET /anomalies?user_id=user_001 — Flagged unusual transactions
- GET /insights?user_id=user_001&month=3&year=2026 — Full report with KPIs and LLM narrative

---

## KPIs Tracked

- **Total spend and income** — net financial position for the period
- **Spend by category** — food, rent, groceries, transport, subscriptions, shopping, health, travel
- **Top merchants** — highest spend merchants ranked by total amount
- **Recurring spend** — subscriptions, rent, and utilities isolated from one-time purchases
- **Anomalies** — transactions flagged as unusually large for their category

---

## Taking This to Production

- **Data source** — replace CSV with Plaid API or open banking feed
- **Database** — replace SQLite with PostgreSQL
- **Pipeline** — replace manual ingestion with scheduled Airflow or dbt job
- **Hosting** — Dockerize and deploy on AWS ECS or Cloud Run
- **Secrets** — move API keys to AWS Secrets Manager or Azure Key Vault
- **LLM** — swap to Azure OpenAI private endpoint for data privacy compliance
- **Auth** — add OAuth2 so each user only sees their own data
- **Personalization** — store user preferences and budget targets to make nudges more specific
- **Notifications** — push weekly insight summaries via email or mobile push notification

---

## Tech Stack

- Python 3.7+
- SQLite — lightweight local data store
- OpenAI GPT-4o-mini — narrative and insight generation
- FastAPI + Uvicorn — REST API layer
- python-dotenv — environment config