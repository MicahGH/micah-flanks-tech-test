Technical Test — Backend Engineer (Mid/Senior)
Context
You are onboarding new bank entities into our data aggregation platform. You receive a CSV file with raw transactions and must build the pipeline that normalizes, persists, and exposes them via API.

The attached CSV (flanks_test_transactions.csv) contains ~530 transactions from 3 different entities across 7 accounts. Real-world data is rarely clean — handling whatever you find in it gracefully is part of the exercise.

What to deliver
1. Ingest & normalize
A script or endpoint that reads the CSV and persists records to a database using a schema you design and justify. Parse the CSV directly — don't rely on libraries that silently swallow malformed rows.

2. REST API with at least:
GET /transactions?account_id=X&from=YYYY-MM-DD&to=YYYY-MM-DD
GET /transactions/summary?account_id=X — returns total balance, total credits, total debits
3. In-memory cache
Cache expensive aggregations. The cache must not persist after the app restarts.

4. Docker
A docker-compose.yml such that docker compose up starts everything. No manual setup steps beyond that.

5. Tests
Include tests. What and how much to test is up to you.

6. README
Explain:

Your schema decisions and trade-offs
How you handle duplicates and malformed rows
What you would add or change before putting this in production
7. Git history
Commit as you work. Meaningful commits that tell a story — not one big blob at the end.

Constraints
Language: Python
Time
Estimated 3–4 hours. We value clarity and good decisions over completeness — a clean, well-explained solution that covers 80% is better than a rushed one that covers 100%.

If anything is ambiguous, make a decision and document it in the README. That's part of what we're evaluating.
