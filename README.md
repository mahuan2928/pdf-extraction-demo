# pdf-extraction-demo

A tiny, free demo of batch PDF data extraction: point it at a folder of
text-based invoice PDFs and get a CSV with the invoice number, date and
total for each file. One Python file, three regexes, no config, no magic.

```bash
python extract.py --input ./samples --out results.csv
```

```
filename,invoice_number,invoice_date,total_amount,status
invoice_001.pdf,INV-2026-001,2026-01-15,1100.00,ok
invoice_002.pdf,INV-2026-002,2026-02-03,560.00,ok
```

If a field isn't found in a PDF, the row is still written — the field is
left empty and the `status` column says what's missing
(e.g. `missing: total_amount`). Nothing is silently dropped.

## Quickstart

```bash
pip install -r requirements.txt

# 1. Generate the 2 synthetic sample invoices (or drop your own PDFs in a folder)
python make_sample.py

# 2. Extract
python extract.py --input ./samples --out results.csv

# 3. Verify against the known-correct output
diff results.csv expected_output.csv   # no output = perfect match
```

Requirements: Python 3.10+. Works on text-based PDFs (the kind produced by
accounting software). Scanned/image PDFs need OCR — see the full version.

## Free demo vs Full version

This demo is the 20-line idea. The full version is the production tool:

| | Free demo (this repo) | [Full version — $39](https://mahuan220.gumroad.com/l/yilvrj) |
|---|---|---|
| Fields | 3 hardcoded (number, date, total) | **Any fields**, defined in `fields.yaml` — no code changes |
| Output | CSV only | CSV **and Excel** (.xlsx) |
| Validation | ✗ | Required fields, value ranges, **cross-field arithmetic** (e.g. total = subtotal + tax) |
| Review workflow | `status` column notes | **Validation report + "needs human review" list** |
| Confidence scores | ✗ | Per-field confidence, low scores flagged |
| Scanned PDFs | ✗ (text-based only) | **OCR path** for scanned PDFs |
| Sample data | 2 synthetic invoices | Synthetic invoices incl. one with a deliberately wrong total, so you can watch validation catch it |
| License | MIT | One commercial project per license |

👉 **Get the full version: [PDF & Invoice Data Extraction Pipeline — $39 on Gumroad](https://mahuan220.gumroad.com/l/yilvrj)**

## How it works

`extract.py` opens each PDF with [pdfplumber](https://github.com/jsvine/pdfplumber),
concatenates the page text, and applies one anchored regex per field
(the `Total:` pattern is anchored to line start so `Subtotal:` can't
match by accident). Amounts are normalized (`1,100.00` → `1100.00`).
That's genuinely all of it — read the file, it's ~100 lines.

## Author

Built by **Marty Ma** — Senior AI & Data Engineer (Tokyo). I build
production AI and data pipelines for enterprise clients; this demo is a
miniature of the extraction tooling I use on paid engagements.

## License

MIT — see [LICENSE](LICENSE). The full version above is a separate
commercial product.
