# PRD: PFM Insights — LLM Copilot

**Author:** Varun Nair
**Status:** v1.0 — Complete
**Last Updated:** March 2026

---

## Problem Statement

Personal finance management tools have existed for over a decade — Mint, YNAB, Personal Capital — yet financial literacy and healthy spending habits remain a challenge for most people. The core issue is not access to data. Most people can see their transactions. The issue is that raw data does not tell you what to do.

Current tools show you a pie chart of your spending. They do not tell you that your food spend jumped 40% this month, that your subscriptions are quietly compounding, or that one anomalous transaction on a Tuesday is worth investigating. And they certainly do not give you a specific, friendly nudge that feels like advice from a financially savvy friend.

There is a gap between transaction data and actionable financial guidance. LLMs close that gap.

---

## Target Users

- **Young professionals** — earning a salary, spending across multiple categories, want to understand where their money goes without building a spreadsheet
- **Neobank or fintech product teams** — want to add an AI-powered insights layer on top of existing transaction data
- **Plaid-connected app developers** — building consumer finance apps and want a narrative layer over raw API data
- **Personal use** — anyone who wants a monthly financial summary that reads like advice, not a dashboard

---

## Goals

**Primary Goals**
- Automatically generate a plain-English monthly financial summary from raw transaction data
- Surface spending anomalies without requiring the user to manually review transactions
- Provide one specific, actionable nudge per summary to drive a behavior change

**Secondary Goals**
- Build a reusable API so this can power a mobile app, Slack bot, or weekly email digest
- Demonstrate a production-ready architecture for LLM-augmented personal finance products

**Non-Goals for v1**
- Real bank connections (no Plaid API integration yet)
- User accounts, login, or authentication
- Budget setting or goal tracking
- Investment or savings account data
- Real-time transaction processing

---

## Success Metrics

- **Narrative quality** — LLM output references the correct categories, amounts, and anomalies from the actual data
- **Anomaly relevance** — flagged transactions are genuinely unusual relative to the user's spending patterns
- **API response time** — /insights endpoint returns in under 5 seconds
- **Coverage** — all major spending categories represented and correctly attributed
- **Reusability** — any user_id can be queried independently with correct isolation

---

## Scope — What Is In v1

- CSV ingestion into SQLite with full transaction schema
- Global financial summary: total spend, income, net position, average transaction
- Spend breakdown by category and top merchants
- Recurring spend isolation (subscriptions, rent, utilities)
- Anomaly flagging for unusually large transactions by category
- Optional filtering by user, month, and year
- LLM-generated narrative via OpenAI GPT-4o-mini with friendly tone and one actionable nudge
- CLI entrypoint supporting user, month, and year arguments
- FastAPI REST API with four endpoints: /health, /summary, /anomalies, /insights
- Synthetic data generator covering 6 months of realistic personal transactions

## Scope — What Is Out of v1

- Real bank or Plaid API connection
- Multi-user authentication and data isolation at the API layer
- Historical month-over-month comparison and trend analysis
- Budget targets and goal progress tracking
- Push notifications or email digest delivery
- Investment, savings, or loan account tracking
- Frontend UI

---

## Feature Breakdown

**1. Data Ingestion**
Loads a CSV of personal transactions into SQLite. Schema covers transaction ID, date, amount, currency, merchant name, category, transaction type (debit or credit), account type, user ID, month, year, recurring flag, and anomaly flag.

**2. KPI Computation**
Computes the following metrics with optional user, month, and year filtering: total spend and income with net position, spend broken down by category, top 5 merchants by spend, total recurring spend and count, and list of flagged anomalous transactions.

**3. Anomaly Detection**
Transactions are flagged as anomalies during data generation when their amount is significantly above the normal range for their category. In production this would use a rolling baseline per user and category to dynamically detect spikes.

**4. LLM Narrative Generation**
Builds a structured prompt from the full KPI snapshot and sends it to GPT-4o-mini. The prompt instructs the model to act as a personal finance advisor and produce a 4-5 sentence summary covering overall financial health, biggest spending category, any unusual transactions, and one specific actionable nudge.

**5. REST API**
Four endpoints via FastAPI. GET /health for liveness. GET /summary for raw KPI breakdown. GET /anomalies for flagged transactions. GET /insights for the full report including LLM narrative.

**6. CLI**
Command: python -m src.cli [user_id] [month] [year]. Prints full snapshot and narrative to terminal. Suitable for local use or scheduled reporting jobs.

---

## Technical Architecture

Data flows in one direction:

transactions_raw.csv → ingestion.py → transactions.db → metrics.py → KPI dict → reporter.py → LLM prompt → llm_client.py → OpenAI API → narrative → cli.py or api.py → output

Stack: Python 3.7+, SQLite, OpenAI GPT-4o-mini, FastAPI, Uvicorn, python-dotenv

---

## Production Roadmap

- **Data source** — replace CSV with Plaid API or open banking connection
- **Database** — replace SQLite with PostgreSQL with per-user row-level security
- **Pipeline** — replace manual ingestion with Airflow DAG running nightly
- **Anomaly detection** — replace static flag with dynamic rolling baseline per user and category
- **Hosting** — Dockerize and deploy on AWS ECS or Cloud Run
- **Secrets** — move to AWS Secrets Manager or Azure Key Vault
- **LLM** — move to Azure OpenAI private endpoint for financial data privacy compliance
- **Auth** — add OAuth2 so each user only accesses their own data
- **Personalization** — store user budget targets and preferences to make nudges more specific
- **Delivery** — weekly insight digest via email or mobile push notification
- **Evals** — add LLM output evaluation to ensure narrative accuracy and tone consistency

---

## Open Questions

1. Should anomaly thresholds be static or dynamically computed per user based on their own spending history?
2. Should the narrative be cached per user per month to avoid redundant LLM calls on repeated requests?
3. How should multi-currency transactions be handled in the spend aggregations?
4. Should the /insights endpoint support a webhook so the narrative can be pushed rather than polled?
5. At what point does the per-user data volume require moving from SQLite to a proper relational database?