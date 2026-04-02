#!/usr/bin/env python3
"""Run OCR on a PDF via ocrmypdf when available."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def build_command(input_pdf: Path, output_pdf: Path, lang: str, force_ocr: bool) -> list[str] | None:
    binary = shutil.which("ocrmypdf")
    if binary:
        cmd = [binary]
    else:
        cmd = [sys.executable, "-m", "ocrmypdf"]
        probe = subprocess.run(cmd + ["--version"], capture_output=True, text=True)
        if probe.returncode != 0:
            return None

    command = cmd + ["-l", lang]
    if force_ocr:
        command.append("--force-ocr")
    command.extend([str(input_pdf), str(output_pdf)])
    return command


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_pdf", type=Path, help="Source PDF")
    parser.add_argument("output_pdf", type=Path, help="OCR output PDF")
    parser.add_argument("--lang", default="chi_sim+eng", help="OCR language pack name")
    parser.add_argument("--force-ocr", action="store_true", help="Force OCR even if text exists")
    args = parser.parse_args()

    command = build_command(args.input_pdf, args.output_pdf, args.lang, args.force_ocr)
    if command is None:
        print(
            "ocrmypdf is not available. Install it before running OCR. "
            "See references/tooling.md for the preferred dependency path.",
            file=sys.stderr,
        )
        sys.exit(2)

    result = subprocess.run(command)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
