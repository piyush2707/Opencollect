# OpenCollect


[![Tests](https://github.com/piyush2707/Opencollect/actions/workflows/tests.yml/badge.svg)](https://github.com/piyush2707/Opencollect/actions/workflows/tests.yml)


**An open-source, developer-first toolkit for invoice follow-ups.**

OpenCollect is an early-stage Python project for small businesses and developers who want to identify overdue invoices and prepare polite, reviewable payment reminders. The first release focuses on a small, dependable core that works locally and does not require an AI API key.

> **Project status:** MVP starter. CSV parsing and overdue-invoice detection are implemented. Reminder sending, AI integrations, web UI, and FastAPI endpoints are planned, not implemented.

## Why OpenCollect?

Many small businesses track unpaid invoices in spreadsheets and follow up manually. OpenCollect aims to make the first steps easier:

1. Read invoice data from a CSV file.
2. Validate important fields.
3. Find unpaid invoices whose due date has passed.
4. Print a clear report.
5. Later, prepare reminder drafts that a person reviews before sending.

This project does **not** send messages, collect money, access bank accounts, or confirm payments.

## Features in this starter

- [x] CSV invoice import using Python's standard library
- [x] Required-field and basic data validation
- [x] Overdue invoice detection
- [x] Stable report ordering
- [x] Command-line report
- [x] Fictional sample data
- [x] Unit tests
- [ ] Editable reminder templates
- [ ] Hindi and English reminder templates
- [ ] Optional AI reminder adapter
- [ ] FastAPI endpoints
- [ ] Accounting and messaging integrations

## Requirements

- Python 3.10 or newer
- No third-party dependencies for the core library
- A terminal or command prompt to run the commands below

## Quick start

### 1. Download or clone this repository

```bash
git clone https://github.com/piyush2707/Opencollect.git
cd Opencollect
```

Alternatively, download the ZIP from GitHub and extract it.

### 2. Run the tests

```bash
python -m unittest discover -s tests -v
```

On some systems, use `python3` instead of `python`.

### 3. Run the sample report

```bash
python -m opencollect.cli examples/invoices.csv --as-of 2026-10-22
```

The `--as-of` argument makes the report reproducible. Omit it to use the computer's current date.

## CSV format

The CSV needs these columns:

| Column | Required | Meaning | Example |
|---|---|---|---|
| `invoice_id` | Yes | Unique invoice identifier | `INV-1001` |
| `customer` | Yes | Customer or business name | `Sunrise Traders` |
| `amount` | Yes | Non-negative amount, using a decimal point | `18500.00` |
| `due_date` | Yes | Due date in `YYYY-MM-DD` format | `2026-10-15` |
| `status` | Yes | Payment status | `unpaid` |

Example:

```csv
invoice_id,customer,amount,due_date,status
INV-1001,Sunrise Traders,18500.00,2026-10-15,unpaid
INV-1002,Northstar Services,7200.00,2026-10-25,unpaid
INV-1003,Mehta Components,12400.00,2026-10-01,paid
```

Status values such as `paid`, `settled`, `complete`, and `completed` are treated as paid, case-insensitively. Other statuses are treated as unpaid for the initial MVP. In a production system, replace this permissive behavior with an explicit status allow-list and reconciliation process.

An invoice is considered overdue only when it is unpaid and its due date is **earlier than** the report's `as_of` date. An invoice due today is not yet overdue.

## Python usage

```python
from datetime import date
from opencollect import load_invoices, overdue_invoices

invoices = load_invoices("examples/invoices.csv")
late = overdue_invoices(invoices, as_of=date(2026, 10, 22))

for invoice in late:
    print(invoice.invoice_id, invoice.customer, invoice.amount)
```

## Project structure

```text
opencollect/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
├── .gitignore
├── opencollect/
│   ├── __init__.py
│   ├── invoices.py
│   └── cli.py
├── examples/
│   └── invoices.csv
├── tests/
│   └── test_invoices.py
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── workflows/
        └── tests.yml
```

## Privacy and safety principles

- Use fictional or anonymised data while testing.
- Do not commit real customer invoices, phone numbers, email addresses, bank details, credentials, or API keys.
- Review any customer-facing message before sending it.
- Do not claim a payment was received unless a trusted source confirms it.
- Keep a human in control of collection decisions.
- Follow applicable privacy, consumer-protection, messaging, and business rules before deploying integrations.

## Roadmap

### Milestone 1 — Reliable local core
- CSV import and validation
- Overdue report
- Unit tests

### Milestone 2 — Reminder drafts
- Polite, editable templates
- English and Hindi variants
- Tone controls without threats or misleading claims
- Tests ensuring invoice values are copied correctly

### Milestone 3 — Developer integration
- Optional FastAPI endpoints
- API documentation
- Sample client
- Authentication and rate limits before any public deployment

### Milestone 4 — Optional AI
- Provider-neutral interface
- AI-generated drafts only; no automatic sending by default
- Clear fallback when no API key is configured
- Tests for hallucinated payment claims and sensitive data leakage

### Milestone 5 — Learn from users
- Interview small distributors, agencies, and manufacturers
- Identify which workflow is most painful
- Prioritise integrations only after demand is demonstrated

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md). For bugs and feature ideas, use GitHub Issues.

## Security

Please read [SECURITY.md](SECURITY.md). Never publish secrets or real financial records in issues.

## License

OpenCollect is licensed under the MIT License. See [LICENSE](LICENSE).
