# Flanks Backend Technical Test

Backend service that imports bank transactions from CSV files, normalizes the data, stores it in PostgreSQL, and exposes a REST API.

## Stack

- Python
- FastAPI
- SQLModel / SQLAlchemy
- PostgreSQL
- Pydantic
- Docker Compose
- Pytest

## Running

Start the application:

    docker compose up

Run tests:

    pytest

## Database Design

The schema contains two main tables:

### Account

Stores bank account information:

- `id`: Internal identifier.
- `external_account_id`: Bank-provided account identifier.
- `entity`: Bank entity.
- `iban`: Account IBAN.

### Transaction

Stores normalized transactions:

- `transaction_id`: Unique bank transaction identifier.
- `account_id`: Foreign key to the table `account`.
- `operation_date` and `value_date`.
- `amount` and `balance` using `Decimal`.
- `currency`, `category`, and `transaction` metadata.

## Design Decisions

- Internal IDs are used instead of external identifiers to avoid coupling the database to external systems.
- `Decimal` is used for financial values to avoid floating point precision issues.
- Account data is normalized to avoid duplicating account information in every transaction.
- The `transaction` table could be normalized even more but for the purpose of this test, it is fine.
- I have separated the logic out so that if a new format of data comes through, it is extremely easy to create, for example, a JSONParser. The services don't need to know anything about the parsers nor the repositories and vice-verse.

## Import & Normalization

CSV rows are parsed directly and validated using Pydantic.

The importer handles:

- ISO dates plus unambiguous `YYYY/MM/DD`, `DD-MM-YYYY`, and `DD/MM/YYYY`
  dates. Ambiguous values such as `04/06/2024`, blank dates, and unsupported
  formats are recorded as malformed instead of being guessed.
  A production importer could use an entity-to-format map once each bank's
  export contract is known; that would allow otherwise ambiguous values to be
  parsed safely according to their source entity rather than applying one
  global guess.
- Currency and category normalization.
- A controlled entity vocabulary (`santander`, `sabadell`, and `lacaixa`). This
  intentionally rejects unrecognised labels such as `BBVA`, `B.B.V.A`, or
  `Banco Santander`: accepting them would create inconsistent entities. Their
  rows are retained as malformed, and can be reprocessed after an explicit
  entity or alias mapping is added.
- Different decimal formats (`1,234.56`, `1.234,56`, etc.).
  A value using only one separator with three trailing digits (for example,
  `1,234` or `1.234`) is rejected because it could mean either a decimal or a
  thousands separator.
- Required transaction, account, and IBAN identifiers.
- Unknown columns, so an upstream CSV schema change is visible immediately.

Malformed rows are skipped and counted instead of stopping the whole import process.

## Duplicate Handling

Transactions are considered duplicates when they have the same `transaction_id`.

The database enforces this using a unique constraint:

    transaction_id UNIQUE

Imports use `ON CONFLICT DO UPDATE`, making the import process idempotent.

## API

### Get transactions

    GET /transactions?account_id={id}&from={date}&to={date}

### Get transaction summary

    GET /transactions/summary?account_id={id}

Returns:

- Total balance.
- Total credits.
- Total debits.

## Cache

Transaction summaries use an in-memory TTL cache.

The cache:

- Exists only while the application is running.
- Is lost after application restarts.
- Avoids repeated expensive database aggregations.

For a production environment with multiple application instances, this would be replaced with a distributed cache such as Redis.

## Tests

Tests cover:

- Transaction normalization.
- Invalid data handling.
- Account creation.
- Duplicate transaction handling.
- API endpoints.
- Cache behaviour.

## Production Improvements

Before production I would add:

- Database migrations with Alembic.
- Better observability with logs and metrics, for example, letting the importer know what rows, objects, etc. of the uploaded file are malformed and how.
- Distributed cache (Redis).
- Background processing for large imports. Maybe queues using RabbitMQ.
- Authentication and authorization.
- More integration and unit tests.
- GitHub Actions CI/CD pipeline before deployment
