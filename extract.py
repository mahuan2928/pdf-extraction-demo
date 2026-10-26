"""pdf-extraction-demo — pull 3 fields out of a folder of invoice PDFs.

Usage:
    python extract.py --input ./samples --out results.csv

For every text-based PDF in --input, this extracts three hardcoded fields
with regular expressions and writes one CSV row per file:

    filename, invoice_number, invoice_date, total_amount, status

If a field can't be found, the row is still written with that field left
empty and the missing fields named in the `status` column (e.g.
"missing: total_amount") — nothing is silently dropped.

This is a free demo. The full version defines any fields you want in a
YAML config, validates them, and writes Excel + review reports:
https://mahuan220.gumroad.com/l/yilvrj
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("ERROR: pdfplumber is not installed. Run: pip install -r requirements.txt")

# The whole "configuration" of the demo: one regex per field.
# (The full version moves these into fields.yaml so you can extract
# any fields from any document layout without touching code.)
FIELDS = {
    "invoice_number": re.compile(
        r"Invoice\s*(?:No\.?|Number|#)\s*[:#]?\s*([A-Za-z0-9\-]+)", re.IGNORECASE
    ),
    "invoice_date": re.compile(
        r"\bDate\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE
    ),
    # Anchored to line start so "Subtotal:" doesn't match as the total.
    "total_amount": re.compile(
        r"^\s*Total\s*:\s*\$?\s*([\d,]+\.\d{2})", re.IGNORECASE | re.MULTILINE
    ),
}


def pdf_text(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_one(path: Path) -> dict:
    row = {"filename": path.name}
    missing = []
    try:
        text = pdf_text(path)
    except Exception as exc:  # unreadable/corrupt PDF: note it, don't crash
        row.update({name: "" for name in FIELDS})
        row["status"] = f"error: could not read PDF ({exc.__class__.__name__})"
        return row
    for name, pattern in FIELDS.items():
        m = pattern.search(text)
        if m:
            # Normalize amounts: "1,100.00" -> "1100.00"
            row[name] = m.group(1).replace(",", "") if name == "total_amount" else m.group(1)
        else:
            row[name] = ""
            missing.append(name)
    row["status"] = "ok" if not missing else "missing: " + ", ".join(missing)
    return row


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract invoice fields from a folder of PDFs.")
    ap.add_argument("--input", default="./samples", help="Folder containing PDF files")
    ap.add_argument("--out", default="results.csv", help="CSV file to write")
    args = ap.parse_args()

    pdfs = sorted(Path(args.input).glob("*.pdf"))
    if not pdfs:
        sys.exit(f"ERROR: no PDF files found in {args.input}")

    rows = []
    for pdf in pdfs:
        row = extract_one(pdf)
        print(f"{pdf.name}: {row['status']}")
        rows.append(row)

    columns = ["filename", *FIELDS, "status"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    ok = sum(1 for r in rows if r["status"] == "ok")
    print(f"\n{ok}/{len(rows)} files fully extracted -> {args.out}")


if __name__ == "__main__":
    main()
