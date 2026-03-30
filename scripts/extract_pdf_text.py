#!/usr/bin/env python3
"""Extract page-by-page text from a PDF into JSON or plain text."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CAPTION_PATTERNS = (
    re.compile(r"^\s*(figure|fig\.)\s*\d+", re.IGNORECASE),
    re.compile(r"^\s*table\s*\d+", re.IGNORECASE),
)


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


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def analyze_page_text(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    line_count = len(lines)
    short_lines = [line for line in lines if len(line) <= 12]
    short_line_ratio = (len(short_lines) / line_count) if line_count else 0.0
    avg_line_length = (sum(len(line) for line in lines) / line_count) if line_count else 0.0
    has_caption = any(pattern.search(line) for pattern in CAPTION_PATTERNS for line in lines)

    flags: list[str] = []
    if len(text) < 40:
        flags.append("low_text")
    if has_caption:
        flags.append("caption_like")
    if line_count >= 20 and short_line_ratio >= 0.45:
        flags.append("fragmented_layout")
    if line_count >= 20 and avg_line_length <= 18:
        flags.append("dense_short_lines")

    return {
        "line_count": line_count,
        "avg_line_length": round(avg_line_length, 2),
        "short_line_ratio": round(short_line_ratio, 3),
        "flags": flags,
    }


def extract_with_pdfplumber(pdf_path: Path, selected_pages: list[int] | None) -> list[dict]:
    import pdfplumber

    pages: list[dict] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        total_pages = len(pdf.pages)
        page_numbers = selected_pages or list(range(1, total_pages + 1))
        for page_number in page_numbers:
            if page_number > total_pages:
                raise ValueError(f"Requested page {page_number}, but PDF has only {total_pages} pages")
            raw_text = pdf.pages[page_number - 1].extract_text() or ""
            text = clean_text(raw_text)
            analysis = analyze_page_text(text)
            pages.append(
                {
                    "page": page_number,
                    "char_count": len(text),
                    "word_count": len(text.split()),
                    "line_count": analysis["line_count"],
                    "avg_line_length": analysis["avg_line_length"],
                    "short_line_ratio": analysis["short_line_ratio"],
                    "flags": analysis["flags"],
                    "text": text,
                }
            )
    return pages


def extract_with_pypdf2(pdf_path: Path, selected_pages: list[int] | None) -> list[dict]:
    from PyPDF2 import PdfReader

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    page_numbers = selected_pages or list(range(1, total_pages + 1))
    pages: list[dict] = []
    for page_number in page_numbers:
        if page_number > total_pages:
            raise ValueError(f"Requested page {page_number}, but PDF has only {total_pages} pages")
        raw_text = reader.pages[page_number - 1].extract_text() or ""
        text = clean_text(raw_text)
        analysis = analyze_page_text(text)
        pages.append(
            {
                "page": page_number,
                "char_count": len(text),
                "word_count": len(text.split()),
                "line_count": analysis["line_count"],
                "avg_line_length": analysis["avg_line_length"],
                "short_line_ratio": analysis["short_line_ratio"],
                "flags": analysis["flags"],
                "text": text,
            }
        )
    return pages


def build_payload(pdf_path: Path, pages: list[dict], extractor: str) -> dict:
    low_text_pages = [item["page"] for item in pages if "low_text" in item["flags"]]
    visual_hint_pages = [
        item["page"]
        for item in pages
        if any(flag in item["flags"] for flag in ("low_text", "caption_like", "fragmented_layout", "dense_short_lines"))
    ]
    return {
        "source_pdf": str(pdf_path.resolve()),
        "extractor": extractor,
        "page_count": len(pages),
        "low_text_pages": low_text_pages,
        "visual_hint_pages": visual_hint_pages,
        "pages": pages,
    }


def write_text_output(payload: dict, txt_out: Path) -> None:
    lines: list[str] = []
    for page in payload["pages"]:
        lines.append(f"===== Page {page['page']} =====")
        lines.append(page["text"])
        lines.append("")
    txt_out.parent.mkdir(parents=True, exist_ok=True)
    txt_out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract page-by-page text from a PDF.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--pages", help="Pages like 1,3-5", default=None)
    parser.add_argument("--json-out", help="Write JSON output to this file")
    parser.add_argument("--txt-out", help="Write plain-text output to this file")
    parser.add_argument(
        "--output-root",
        help="Write default outputs under this root as <root>/<pdf-name>/paper.json and paper.txt",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.is_file():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    try:
        selected_pages = parse_pages(args.pages)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        pages = extract_with_pdfplumber(pdf_path, selected_pages)
        extractor = "pdfplumber"
    except Exception:
        try:
            pages = extract_with_pypdf2(pdf_path, selected_pages)
            extractor = "PyPDF2"
        except Exception as exc:
            print(f"Failed to extract text: {exc}", file=sys.stderr)
            return 1

    payload = build_payload(pdf_path, pages, extractor)

    json_out = Path(args.json_out) if args.json_out else None
    txt_out = Path(args.txt_out) if args.txt_out else None

    if args.output_root:
        auto_dir = default_output_dir(pdf_path, args.output_root)
        if json_out is None:
            json_out = auto_dir / "paper.json"
        if txt_out is None:
            txt_out = auto_dir / "paper.txt"

    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if txt_out:
        write_text_output(payload, txt_out)

    if not json_out and not txt_out:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"Extracted {payload['page_count']} page(s) with {payload['extractor']}. "
            f"Low-text pages: {payload['low_text_pages']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
