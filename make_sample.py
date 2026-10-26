"""Generate the 2 synthetic sample invoices used by the smoke test.

    python make_sample.py            # writes ./samples/invoice_001.pdf, invoice_002.pdf

No real data — vendor, customer and numbers are made up. The matching
correct extraction is in expected_output.csv, so you can run extract.py
on ./samples and diff the result to verify everything works.
"""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
except ImportError:
    raise SystemExit("ERROR: reportlab is not installed. Run: pip install -r requirements.txt")


def make_invoice(path: Path, *, number: str, date: str, vendor: str,
                 bill_to: str, total: float) -> None:
    c = canvas.Canvas(str(path), pagesize=A4)
    y = 780
    lines = [
        ("INVOICE", 18),
        (f"Invoice No: {number}", 12),
        (f"Date: {date}", 12),
        (f"Vendor: {vendor}", 12),
        (f"Bill To: {bill_to}", 12),
        ("", 12),
        ("Description: Consulting services", 12),
        (f"Total: ${total:,.2f}", 14),
    ]
    for text, size in lines:
        c.setFont("Helvetica-Bold" if size >= 14 else "Helvetica", size)
        c.drawString(60, y, text)
        y -= 28
    c.showPage()
    c.save()
    print(f"wrote {path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="./samples", help="Folder to write sample PDFs into")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    make_invoice(out / "invoice_001.pdf", number="INV-2026-001", date="2026-01-15",
                 vendor="ACME Supplies Ltd.", bill_to="Globex Corporation", total=1100.00)
    make_invoice(out / "invoice_002.pdf", number="INV-2026-002", date="2026-02-03",
                 vendor="ACME Supplies Ltd.", bill_to="Initech LLC", total=560.00)

    print("\nNow run:\n  python extract.py --input", args.out, "--out results.csv")
    print("  diff results.csv expected_output.csv   # should print nothing")


if __name__ == "__main__":
    main()
