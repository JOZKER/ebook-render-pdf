# Tooling Notes

Use this file only when local PDF or OCR tooling is missing.

## Preferred stack

1. `pypdf`
   Use for fast PDF inspection and text-coverage heuristics.

2. `pymupdf`
   Use for page rendering, embedded-image extraction, and page-region crops.

3. `ocrmypdf`
   Prefer for OCR because it preserves the original PDF while adding a searchable text layer.

## Typical install commands

```powershell
python -m pip install pypdf pymupdf
python -m pip install ocrmypdf
```

`ocrmypdf` may still require external OCR components depending on the platform.
If `ocrmypdf` is unavailable, say so clearly and stop rather than pretending OCR succeeded.

## Practical rules

- Keep the original PDF even after OCR.
- Use OCR only to recover text, not to replace visual inspection.
- When OCR output is noisy, keep chapter titles and formulas aligned with the original page images.
- If the PDF mixes native text pages and scanned pages, OCR the document copy anyway if that is faster than handling pages separately, but still inspect the original pages for visuals.
