# PDF Visualization

Use this file when you need guidance about screenshots, rendered pages, or extraction failures.

## Why PDF Extraction Breaks

Common reasons:

- the PDF stores layout positions instead of semantic structure
- double-column reading order gets mixed
- formulas are stored as vector objects or images
- tables are only loose text blocks and lines
- scanned pages require OCR
- unusual fonts produce garbled copied text

Do not treat these issues as a pure model failure. They usually come from the source file plus the extraction path.

## When To Switch To Images

Switch early when:

- symbols are missing
- a figure is central to the question
- a table loses rows or columns
- the extracted page is nearly empty
- the user already points to a specific region on the page

## Practical Workflow

1. Use `scripts/extract_pdf_text.py` for an initial text pass.
2. If confidence drops, use `scripts/render_pdf_pages.py` on the relevant page.
3. If the target is still too dense, ask the user for a cropped screenshot.
4. Explain what is certain and what still needs visual confirmation.

## Working In VS Code

- Open the PDF directly in VS Code so the user can read the original layout.
- Open rendered PNG pages side by side when a page needs visual explanation.
- Refer to page numbers and section names so the user can jump back to the original PDF quickly.

## Working In Terminal-First Flows

- Render relevant pages to PNG files.
- Use local image viewing tools when available.
- If the user cannot easily open the PNG, ask for a screenshot taken from their PDF viewer instead.
