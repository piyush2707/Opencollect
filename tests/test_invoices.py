from datetime import date
from decimal import Decimal
from io import StringIO
import unittest

from opencollect.invoices import (
    InvoiceValidationError,
    load_invoices,
    overdue_invoices,
)


class InvoiceTests(unittest.TestCase):
    def test_load_and_find_overdue(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status\n"
            "INV-1,Example Co,100.50,2026-10-01,unpaid\n"
            "INV-2,Another Co,50,2026-10-22,unpaid\n"
            "INV-3,Paid Co,25,2026-09-01,paid\n"
        )
        invoices = load_invoices(StringIO(csv_data))
        overdue = overdue_invoices(invoices, date(2026, 10, 22))
        self.assertEqual([item.invoice_id for item in overdue], ["INV-1"])
        self.assertEqual(overdue[0].amount, Decimal("100.50"))

    def test_due_today_is_not_overdue(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status\n"
            "INV-1,Example Co,100,2026-10-22,unpaid\n"
        )
        self.assertEqual(
            overdue_invoices(load_invoices(StringIO(csv_data)), date(2026, 10, 22)),
            [],
        )

    def test_paid_invoice_is_not_overdue(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status\n"
            "INV-1,Example Co,100,2026-10-01,paid\n"
        )
        self.assertEqual(
            overdue_invoices(load_invoices(StringIO(csv_data)), date(2026, 10, 22)),
            [],
        )

    def test_invalid_amount_raises(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status\n"
            "INV-1,Example Co,not-money,2026-10-01,unpaid\n"
        )
        with self.assertRaises(InvoiceValidationError):
            load_invoices(StringIO(csv_data))

    def test_negative_amount_raises(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status\n"
            "INV-1,Example Co,-5,2026-10-01,unpaid\n"
        )
        with self.assertRaises(InvoiceValidationError):
            load_invoices(StringIO(csv_data))

    def test_missing_column_raises(self):
        with self.assertRaises(InvoiceValidationError):
            load_invoices(StringIO("invoice_id,customer\nINV-1,Example\n"))

    def test_bad_date_raises(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status\n"
            "INV-1,Example Co,100,not-a-date,unpaid\n"
        )
        with self.assertRaises(InvoiceValidationError):
            load_invoices(StringIO(csv_data))

    def test_duplicate_headers_raise(self):
        csv_data = (
            "invoice_id,customer,amount,due_date,status,status\n"
            "INV-1,Example Co,100,2026-10-01,unpaid,paid\n"
        )
        with self.assertRaises(InvoiceValidationError):
            load_invoices(StringIO(csv_data))


if __name__ == "__main__":
    unittest.main()
