"""CSV invoice loading and overdue detection using only the Python standard library."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, TextIO

_REQUIRED_COLUMNS = {"invoice_id", "customer", "amount", "due_date", "status"}
_PAID_STATUSES = {"paid", "settled", "complete", "completed"}


class InvoiceValidationError(ValueError):
    """Raised when an invoice row is missing or contains invalid fields."""


@dataclass(frozen=True)
class Invoice:
    invoice_id: str
    customer: str
    amount: Decimal
    due_date: date
    status: str

    @property
    def is_paid(self) -> bool:
        return self.status.strip().casefold() in _PAID_STATUSES

    def is_overdue(self, as_of: date) -> bool:
        """Return True when unpaid and due strictly before as_of."""
        return not self.is_paid and self.due_date < as_of


def _parse_row(row: dict[str, str | None], line_number: int) -> Invoice:
    invoice_id = (row.get("invoice_id") or "").strip()
    customer = (row.get("customer") or "").strip()
    raw_amount = (row.get("amount") or "").strip()
    raw_due_date = (row.get("due_date") or "").strip()
    status = (row.get("status") or "").strip()

    values = {
        "invoice_id": invoice_id,
        "customer": customer,
        "amount": raw_amount,
        "due_date": raw_due_date,
        "status": status,
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise InvoiceValidationError(
            f"Line {line_number}: missing required value(s): {', '.join(missing)}"
        )

    try:
        amount = Decimal(raw_amount)
    except InvalidOperation as exc:
        raise InvoiceValidationError(
            f"Line {line_number}: amount must be a valid decimal number"
        ) from exc
    if not amount.is_finite() or amount < 0:
        raise InvoiceValidationError(
            f"Line {line_number}: amount must be finite and non-negative"
        )

    try:
        due_date = date.fromisoformat(raw_due_date)
    except ValueError as exc:
        raise InvoiceValidationError(
            f"Line {line_number}: due_date must use YYYY-MM-DD format"
        ) from exc

    return Invoice(
        invoice_id=invoice_id,
        customer=customer,
        amount=amount,
        due_date=due_date,
        status=status,
    )


def load_invoices(source: str | Path | TextIO) -> list[Invoice]:
    """Load invoices from a CSV path or an already-open text stream."""
    if hasattr(source, "read"):
        return _load_from_stream(source)  # type: ignore[arg-type]
    with Path(source).open("r", newline="", encoding="utf-8-sig") as handle:
        return _load_from_stream(handle)


def _load_from_stream(handle: TextIO) -> list[Invoice]:
    reader = csv.DictReader(handle)
    if not reader.fieldnames:
        raise InvoiceValidationError("CSV file is empty or has no header")

    normalized_headers = [(name or "").strip() for name in reader.fieldnames]
    if len(normalized_headers) != len(set(normalized_headers)):
        raise InvoiceValidationError("CSV contains duplicate column names")

    missing_columns = sorted(_REQUIRED_COLUMNS - set(normalized_headers))
    if missing_columns:
        raise InvoiceValidationError(
            f"CSV is missing required column(s): {', '.join(missing_columns)}"
        )

    invoices: list[Invoice] = []
    for line_number, raw_row in enumerate(reader, start=2):
        row = {((key or "").strip()): value for key, value in raw_row.items()}
        if None in row:
            raise InvoiceValidationError(
                f"Line {line_number}: row has more values than the CSV header"
            )
        invoices.append(_parse_row(row, line_number))
    return invoices


def overdue_invoices(invoices: Iterable[Invoice], as_of: date) -> list[Invoice]:
    """Return unpaid invoices due before as_of, oldest due first."""
    matches = (invoice for invoice in invoices if invoice.is_overdue(as_of))
    return sorted(matches, key=lambda invoice: (invoice.due_date, invoice.invoice_id))
