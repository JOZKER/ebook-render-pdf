#!/usr/bin/env python3
"""Inspect a PDF and estimate whether OCR is required."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


def classify_page(text: str, threshold: int) -> tuple[int, bool]:
    visible = "".join(ch for ch in text if not ch.isspace())
    count = len(visible)
    return count, count >= threshold


def inspect_pdf(pdf_path: Path, threshold: int) -> dict:
    reader = PdfReader(str(pdf_path))
    per_page = []
    text_pages = 0
    image_pages = 0

    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # pragma: no cover - defensive reporting
            text = ""
            error = str(exc)
        else:
            error = None

        text_chars, has_text = classify_page(text, threshold)
        if has_text:
            text_pages += 1

        try:
            image_count = len(list(page.images))
        except Exception:
            image_count = 0
        if image_count:
            image_pages += 1

        per_page.append(
            {
                "page": index,
                "text_chars": text_chars,
                "has_text": has_text,
                "embedded_images": image_count,
                "extract_error": error,
            }
        )

    page_count = len(per_page)
    text_ratio = (text_pages / page_count) if page_count else 0.0
    image_ratio = (image_pages / page_count) if page_count else 0.0

    if text_ratio >= 0.8:
        recommendation = "native_text"
        rationale = "Most pages already expose readable text."
    elif text_ratio <= 0.2:
        recommendation = "ocr_required"
        rationale = "Most pages appear image-only or text extraction is nearly empty."
    else:
        recommendation = "mixed_check"
        rationale = "The PDF appears mixed; inspect sampled pages before deciding."

    return {
        "pdf": str(pdf_path),
        "page_count": page_count,
        "text_pages": text_pages,
        "image_pages": image_pages,
        "text_ratio": round(text_ratio, 4),
        "image_ratio": round(image_ratio, 4),
        "threshold": threshold,
        "recommendation": recommendation,
        "rationale": rationale,
        "pages": per_page,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Path to the source PDF")
    parser.add_argument(
        "--text-threshold",
        type=int,
        default=80,
        help="Minimum non-whitespace characters to count a page as text-bearing",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON only",
    )
    args = parser.parse_args()

    report = inspect_pdf(args.pdf, args.text_threshold)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"PDF: {report['pdf']}")
    print(f"Pages: {report['page_count']}")
    print(f"Text pages: {report['text_pages']} ({report['text_ratio']:.1%})")
    print(f"Pages with embedded images: {report['image_pages']} ({report['image_ratio']:.1%})")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Why: {report['rationale']}")


if __name__ == "__main__":
    main()
