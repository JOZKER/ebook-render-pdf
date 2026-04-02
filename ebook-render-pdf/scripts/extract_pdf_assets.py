#!/usr/bin/env python3
"""Render PDF pages and extract embedded images for figure selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


def sanitize_ext(ext: str) -> str:
    ext = ext.lower().strip(".")
    return ext or "bin"


def extract_assets(pdf_path: Path, outdir: Path, dpi: int, limit: int | None) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    pages_dir = outdir / "pages"
    images_dir = outdir / "images"
    pages_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    manifest = {
        "pdf": str(pdf_path),
        "pages_rendered": [],
        "embedded_images": [],
    }

    total = len(doc)
    if limit is not None:
        total = min(total, limit)

    for page_index in range(total):
        page = doc[page_index]
        page_no = page_index + 1

        pix = page.get_pixmap(matrix=matrix, alpha=False)
        page_path = pages_dir / f"page-{page_no:04d}.png"
        pix.save(page_path)
        manifest["pages_rendered"].append({"page": page_no, "path": str(page_path)})

        for image_index, image_info in enumerate(page.get_images(full=True), start=1):
            xref = image_info[0]
            extracted = doc.extract_image(xref)
            ext = sanitize_ext(extracted.get("ext", "bin"))
            image_path = images_dir / f"page-{page_no:04d}-img-{image_index:02d}.{ext}"
            image_path.write_bytes(extracted["image"])
            manifest["embedded_images"].append(
                {
                    "page": page_no,
                    "xref": xref,
                    "path": str(image_path),
                    "width": extracted.get("width"),
                    "height": extracted.get("height"),
                    "colorspace": extracted.get("colorspace"),
                }
            )

    manifest_path = outdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest["manifest"] = str(manifest_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Path to the source PDF")
    parser.add_argument("--outdir", type=Path, required=True, help="Directory for rendered assets")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI for page previews")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional page limit for quick inspection",
    )
    args = parser.parse_args()

    manifest = extract_assets(args.pdf, args.outdir, args.dpi, args.limit)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
