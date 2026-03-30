#!/usr/bin/env python3
"""Render selected PDF pages to PNG files via pdftoppm."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def safe_stem(path: Path) -> str:
    stem = re.sub(r"[^\w.-]+", "-", path.stem.strip())
    stem = stem.strip(".-")
    return stem or "paper"


def default_output_dir(pdf_path: Path, output_root: str) -> Path:
    return Path(output_root) / safe_stem(pdf_path)


def parse_pages(spec: str | None) -> list[int] | None:
    if not spec:
        return None

    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start < 1 or end < 1 or end < start:
                raise ValueError(f"Invalid page range: {token}")
            pages.update(range(start, end + 1))
        else:
            page = int(token)
            if page < 1:
                raise ValueError(f"Invalid page number: {token}")
            pages.add(page)
    return sorted(pages)


def load_pages_from_json(json_path: Path) -> list[int]:
    if not json_path.is_file():
        raise ValueError(f"JSON metadata not found: {json_path}")

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    pages = payload.get("visual_hint_pages") or payload.get("low_text_pages") or []
    if not isinstance(pages, list) or any(not isinstance(page, int) for page in pages):
        raise ValueError(f"Invalid page metadata in {json_path}")
    return sorted(set(pages))


def render_page(pdf_path: Path, output_dir: Path, page_number: int, dpi: int) -> Path:
    output_base = output_dir / f"page-{page_number:03d}"
    command = [
        "pdftoppm",
        "-png",
        "-r",
        str(dpi),
        "-f",
        str(page_number),
        "-l",
        str(page_number),
        "-singlefile",
        str(pdf_path),
        str(output_base),
    ]
    subprocess.run(command, check=True)
    return output_base.with_suffix(".png")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG files.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--pages", help="Pages like 1,3-5. Default: all pages")
    parser.add_argument(
        "--pages-from-json",
        help="Load visual_hint_pages from extract_pdf_text.py JSON output when --pages is omitted",
    )
    parser.add_argument("--output-dir", help="Directory for PNG files")
    parser.add_argument(
        "--output-root",
        help="Write default outputs under this root as <root>/<pdf-name>/pages",
    )
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI. Default: 180")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.is_file():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    if shutil.which("pdftoppm") is None:
        print("pdftoppm is not available on PATH", file=sys.stderr)
        return 1

    try:
        selected_pages = parse_pages(args.pages)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    doc_dir = default_output_dir(pdf_path, args.output_root) if args.output_root else None

    if selected_pages is None and args.pages_from_json:
        try:
            selected_pages = load_pages_from_json(Path(args.pages_from_json))
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    elif selected_pages is None and doc_dir:
        default_json = doc_dir / "paper.json"
        if default_json.is_file():
            try:
                selected_pages = load_pages_from_json(default_json)
                print(f"Using hinted pages from {default_json.resolve()}")
            except ValueError as exc:
                print(str(exc), file=sys.stderr)
                return 1

    if args.output_dir:
        output_dir = Path(args.output_dir)
    elif doc_dir:
        output_dir = doc_dir / "pages"
    else:
        output_dir = pdf_path.with_name(f"{pdf_path.stem}-pages")
    output_dir.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    pages_to_render = selected_pages
    if pages_to_render is None:
        pages_to_render = [1]
        print("No pages specified. Rendering page 1 by default.")
    elif not pages_to_render:
        print("No hinted pages found in JSON metadata.")
        return 0

    try:
        for page_number in pages_to_render:
            created.append(render_page(pdf_path, output_dir, page_number, args.dpi))
    except subprocess.CalledProcessError as exc:
        print(f"pdftoppm failed: {exc}", file=sys.stderr)
        return 1

    for path in created:
        print(str(path.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
