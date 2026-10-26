# Testing

Smoke test run on 2026-10-26 (Python 3.12.3, venv; demo requires 3.10+).
Dependencies installed from `requirements.txt`: pdfplumber 0.11.10,
reportlab 5.1.0.

## 1. Generate the sample invoices

```bash
pip install -r requirements.txt
python make_sample.py
```

Output:

```
wrote samples/invoice_001.pdf
wrote samples/invoice_002.pdf

Now run:
  python extract.py --input ./samples --out results.csv
  diff results.csv expected_output.csv   # should print nothing
```

## 2. Run the extractor

```bash
python extract.py --input ./samples --out results.csv
```

Output:

```
invoice_001.pdf: ok
invoice_002.pdf: ok

2/2 files fully extracted -> results.csv
```

`results.csv`:

```
filename,invoice_number,invoice_date,total_amount,status
invoice_001.pdf,INV-2026-001,2026-01-15,1100.00,ok
invoice_002.pdf,INV-2026-002,2026-02-03,560.00,ok
```

## 3. Diff against the expected output

```bash
diff results.csv expected_output.csv && echo "DIFF CLEAN - SMOKE TEST PASSED"
```

Output:

```
DIFF CLEAN - SMOKE TEST PASSED
```

(diff printed nothing: byte-identical. Note — an early version of
`extract.py` wrote CRLF line endings via the csv module default and the
diff failed on every line despite identical content; the writer now sets
`lineterminator="\n"`.)

## 4. Missing-field behaviour (extra check)

A test PDF containing only an invoice number and date (no `Total:` line)
was processed separately:

```
partial.pdf: missing: total_amount

0/1 files fully extracted -> out.csv
```

```csv
filename,invoice_number,invoice_date,total_amount,status
partial.pdf,INV-2026-099,2026-03-01,,missing: total_amount
```

The row is written, the missing field is empty, and the gap is named in
the `status` column — as documented in the README.
