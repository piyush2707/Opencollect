"""Command-line report for overdue invoices."""

from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal

from .invoices import InvoiceValidationError, load_invoices, overdue_invoices


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find overdue unpaid invoices in a CSV file."
    )
    parser.add_argument("csv_file", help="Path to invoice CSV")
    parser.add_argument(
        "--as-of",
        type=date.fromisoformat,
        default=date.today(),
        help="Treat this date as today (YYYY-MM-DD); defaults to system date",
    )
    args = parser.parse_args()

    try:
        invoices = load_invoices(args.csv_file)
        overdue = overdue_invoices(invoices, args.as_of)
    except (OSError, InvoiceValidationError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Invoice count: {len(invoices)}")
    print(f"Overdue unpaid invoices as of {args.as_of.isoformat()}: {len(overdue)}")
    print("-" * 72)
    if not overdue:
        print("No overdue unpaid invoices found.")
        return 0

    total = sum((invoice.amount for invoice in overdue), Decimal("0"))
    for invoice in overdue:
        days_late = (args.as_of - invoice.due_date).days
        print(
            f"{invoice.invoice_id} | {invoice.customer} | {invoice.amount:.2f} | "
            f"due {invoice.due_date.isoformat()} | {days_late} day(s) late"
        )
    print("-" * 72)
    print(f"Total overdue amount: {total:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
