---
name: easy-paper
description: Read and explain research papers with a strong focus on PDFs, screenshots, formulas, sections, figures, tables, code blocks, citations, innovation points, and unfamiliar terminology. Use when the user wants a paper map, help understanding a hard section, explanation of a formula, figure, table, code block, citation, or term, or a cumulative reading summary. Treat prompts in the form /easy-paper ... or /ep ... as direct mode selectors for this skill.
argument-hint: "[map|formula|section|figure|table|code|cite|term|summary] [question]"
---

# Easy Paper

Help readers who cannot yet read papers fluently.

Default goal: build a fast mental map of the paper, then explain the hardest parts clearly enough that the user can return to the original paper with confidence.

## Command Shape

Treat the primary interaction forms as:

```text
/easy-paper <mode>
/ep <mode>
```

Supported modes:

- `map`
- `formula`
- `section`
- `figure`
- `table`
- `code`
- `cite`
- `term`
- `summary`

If the user writes `/easy-paper` or `/ep` followed by a longer natural-language request, infer the intended mode from the request.

Note for platform adapters:

- `/easy-paper` is the primary command name exposed by this skill.
- `/ep` is a short alias, but some agent frameworks need a separate alias or command file to make `/ep` discoverable.
- Keep this file as the portable core behavior definition. Put platform-specific alias wiring in adapter files.

## Core Defaults

- Detect the user's preferred language. If the user wants English, answer in English only. If the user wants Chinese, explain in Chinese and keep key English terms when that improves clarity.
- Give source location by default. Prefer page number first. Include section, figure, table, or equation labels when available.
- Use user-meaningful anchors only. Prefer page number, section title or number, figure number, table number, equation number, and nearby claim summary.
- Do not cite raw extracted-text line numbers by default. Avoid references like "lines 683-960" unless the user explicitly asks for line-based quoting or is reading a line-numbered extracted text file instead of the PDF.
- Do not use large line ranges as evidence of precision. If exact local positioning is uncertain, say "around page X", "in Section Y", or "near Figure/Table/Equation Z" instead.
- In whole-paper reading, extract and state the paper's innovation points when the paper clearly presents them. If the paper does not clearly claim innovations or contributions, do not invent them.
- Prefer explanation over raw summarization.
- Prefer accuracy over false precision. If extraction is noisy or a visual element is ambiguous, say so and switch to image-based reading.

## Mode: map

Use when the user starts reading a paper or asks for the paper's overall structure.

1. Extract text from the PDF with `scripts/extract_pdf_text.py`.
2. Keep the extracted text as the primary whole-paper context.
3. Use `visual_hint_pages` from the extraction metadata to render likely figure-heavy, table-heavy, or extraction-broken pages when a full-paper answer needs visual support.
4. Produce this fixed 5-part paper map:
   - paper problem and significance
   - core idea and innovation points
   - method and validation flow
   - reading difficulties
   - suggested next step
5. Cite page numbers throughout and include section names, figure labels, table labels, or equation labels when available. Do not cite raw extracted-text line ranges unless the user explicitly asks for them.
6. Keep sections 1, 2, 4, and 5 concise.
7. Make section 3 the most detailed part of the map. Spend more space on:
   - method stages or pipeline
   - important modules
   - inputs and outputs
   - key formulas or objectives
   - how the paper validates the method
   - what the experiments, ablations, proofs, or case studies are meant to show

## Mode: formula

Use when the user asks about one equation, one loss, one update rule, or one mathematical expression.

Default structure:

1. explain what problem the formula is solving
2. define each symbol or term
3. explain the intuition
4. connect it back to the method
5. derive it only if the user asks or if derivation is essential

If the target formula is unique from context, explain it directly.

If the target formula is ambiguous, do not guess. Ask the user to identify it by one of:

- page number
- section name
- equation number or local formula label
- screenshot

Prefer page number or equation number first. Use screenshot as the most reliable fallback when extraction is noisy, symbols are missing, or the layout is hard to parse.

## Mode: section

Use when the user wants a focused explanation of one section, subsection, or local chapter-like part of the paper.

Treat `section` as a broad user-facing term. It may refer to:

- a numbered section
- a subsection
- a local method block
- an experiment subsection
- a named chapter-like part such as Introduction, Related Work, Method, Experiments, or Conclusion

Default structure:

1. state what this section is trying to do in the paper
2. explain how this section connects to the overall paper flow
3. summarize the key points in order
4. highlight important formulas, figures, tables, or modules in this section
5. explain what the reader should pay most attention to
6. mention likely reading difficulties, hidden assumptions, or easy-to-miss details

If the target section is unique from context, explain it directly.

If the target section is ambiguous, do not guess. Ask the user to identify it by one of:

- page number
- section number
- section title or subsection title
- screenshot

Prefer section number or section title first. Use screenshot as the most reliable fallback when the user only cares about one local region on the page or when extraction quality is low.

## Mode: figure

Use when the user asks about a figure or visual result.

Default structure:

1. state what the figure is showing
2. explain axes, legends, labels, and comparison groups
3. identify the most important pattern
4. tie that pattern back to the paper's claim
5. mention uncertainty if extraction or rendering is incomplete

If the target figure is unique from context, explain it directly.

If the target figure is ambiguous, do not guess. Ask the user to identify it by one of:

- page number
- section name
- figure number or figure title
- screenshot

Prefer page number or figure number first. If the figure is hard to parse from extracted text, render the relevant page with `scripts/render_pdf_pages.py` or ask for a screenshot. Use screenshot as the most reliable fallback when the visual is dense, multi-panel, cropped, or tied to a specific local region.

## Mode: table

Use when the user asks about a table or performance comparison.

Default structure:

1. explain what is being compared
2. explain how to read rows, columns, and metrics
3. identify the key comparison that matters
4. explain what conclusion the authors want the reader to draw
5. note any caveats, fairness issues, or missing context if relevant

If the target table is unique from context, explain it directly.

If the target table is ambiguous, do not guess. Ask the user to identify it by one of:

- page number
- section name
- table number or table title
- screenshot

Prefer page number or table number first. Use screenshot as the most reliable fallback when table structure is lost, rows or columns collapse, or the user only cares about one local part of the table.

## Mode: code

Use when the user asks about an algorithm box, pseudocode block, or step-by-step procedure.

Explain:

1. the inputs and outputs
2. the main stages or loop structure
3. where the key decisions happen
4. which steps correspond to formulas or modules in the paper
5. what implementation intuition the user should keep in mind

If the target code block is unique from context, explain it directly.

If the paper contains multiple code-like blocks or the target is ambiguous, do not guess. Ask the user to identify it by one of:

- page number
- section name
- algorithm number, title, or local heading
- screenshot

Prefer page number or algorithm title first. Use screenshot as the most reliable fallback when layout is complex, the algorithm box is embedded in a dense page, or extraction does not preserve the procedure clearly.

## Mode: cite

Use when the user wants to inspect one cited reference from the paper.

Default structure:

1. give the cited work's bibliographic facts
2. state what kind of work it seems to be
3. explain why the current paper cites it
4. note where it appears in the current paper when that can be identified
5. provide a source link when available
6. suggest whether it is worth reading next

Separate facts from inference clearly.

Treat these as facts when available from the paper or reliable web sources:

- title
- authors
- year
- venue, journal, or conference
- DOI
- arXiv link
- publisher or official paper page

Treat these as inference from the current paper's citation context unless the source states them explicitly:

- whether the cited work is mainly background, a method source, a baseline, or a classic reference
- why the current paper cites it
- where in the current paper it is being used conceptually
- whether it is essential for the user's next reading step

When giving an inference, say that it is based on the current paper's citation context.

When possible, point to where the citation appears in the current paper:

- page number
- section name
- nearby sentence or claim, summarized in your own words

If the exact citation locations cannot be recovered reliably from extraction, say that clearly instead of inventing them.

Use careful web research for citation metadata and links when needed. Prefer reliable scholarly sources such as:

- Crossref
- OpenAlex
- arXiv
- publisher pages
- official project pages

If the target citation is unique from context, explain it directly.

If the target citation is ambiguous, do not guess. Ask the user to identify it by one of:

- reference number
- author name
- title keywords
- screenshot of the reference list or citation marker

Prefer reference number first. Use screenshot as the most reliable fallback when the reference list is noisy or extraction quality is low.

## Mode: term

Use when the user does not understand a term, concept, or background assumption.

1. Check whether the paper itself defines the term clearly.
2. If yes, explain it from the paper and relate it back to the local context.
3. If not, use careful web research to explain the term from reliable sources, then return to how that concept is used in the paper.

Make it clear which part comes from the paper and which part comes from external references.

## Mode: summary

Use when the interaction has become multi-turn or the user explicitly asks for a recap.

Use the template in `references/note-template.md`.

Capture:

- paper identity
- the user's goal
- the paper map
- formulas or visuals that caused difficulty
- clarified points
- remaining open questions
- suggested next reading steps

Do not force note generation after every answer. Generate it directly when the user requests `/easy-paper summary`.

If the current context clearly centers on one paper and contains enough discussion, generate the summary directly.

If the context is too thin, say so briefly and produce a light summary based on what is already known rather than pretending there was a deeper discussion.

If the recent context mixes multiple papers or the target paper is unclear, do not guess. Ask the user to identify the target paper before summarizing.

## Switch From Text To Images When Needed

Treat these as signs that extracted text is not enough:

- double-column text is out of order
- formulas lose symbols or spacing
- tables lose structure
- a page is mostly empty after extraction
- the PDF is scanned
- copied text contains garbled characters
- the question is about a specific local region on the page

When that happens:

1. say that extraction quality is low
2. render the relevant page to PNG with `scripts/render_pdf_pages.py`
3. if needed, ask the user to provide a page screenshot or a cropped screenshot
4. continue with visual-first reading

## Use The Helper Scripts

### Extract PDF Text

```bash
python scripts/extract_pdf_text.py path/to/paper.pdf --json-out out/paper.json --txt-out out/paper.txt
python scripts/extract_pdf_text.py path/to/paper.pdf --output-root out
```

### Render PDF Pages To Images

```bash
python scripts/render_pdf_pages.py path/to/paper.pdf --pages 3,5-6 --output-dir out/pages
python scripts/render_pdf_pages.py path/to/paper.pdf --pages-from-json out/paper.json --output-dir out/pages
python scripts/render_pdf_pages.py path/to/paper.pdf --output-root out
```

When `--output-root out` is used, the scripts keep each PDF isolated under `out/<pdf-name>/`.

## Read Extra References Only When Needed

- Read `references/modes-and-outputs.md` when you want concrete prompt patterns or response shapes.
- Read `references/pdf-visualization.md` when you need guidance about PDF rendering, screenshots, and extraction failures.
- Read `references/note-template.md` when producing a cumulative reading note.
