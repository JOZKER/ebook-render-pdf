---
name: ebook-render-pdf
description: Turn a PDF ebook into a professional Chinese knowledge-summary LaTeX note and rendered PDF. Use when Codex receives a book, paper-like ebook, textbook chapter, scanned PDF, or image-only PDF and must detect whether OCR is needed, preserve and reuse the book's figures instead of ignoring them, extract and reorganize the core knowledge points, and deliver a complete summary package with extracted assets and a compiled PDF. Use especially when the user wants key-point summaries, chapter takeaways, exam review notes, memorization-first notes, or a concise knowledge map derived from a PDF.
---

# Ebook Render PDF

Use this skill to turn a PDF ebook into a complete, compilable `.tex` knowledge-summary note and a rendered PDF.

## Goal

Produce a professional Chinese knowledge-summary note from a PDF book.

The output must:

- use the book's actual content rather than a rough summary
- detect whether the PDF already contains extractable text before deciding to OCR
- preserve the book's figures, diagrams, tables, formulas, and page visuals instead of silently dropping them
- extract the core concepts, definitions, methods, and chapter takeaways rather than writing a reading guide
- reconstruct a teachable knowledge structure with `\section{...}` and `\subsection{...}`
- be a complete `.tex` document from `\documentclass` to `\end{document}`
- compile successfully to PDF as part of delivery

The default output goal is already knowledge-summary first.
When the user asks for exam review, memorization, sprint revision, or a similar mode, compress even further:

- prioritize foundational facts, definitions, lists, and standard short-answer points
- compress or remove extended exposition
- favor headings such as "must memorize", "short-answer template", "high-frequency keywords", and "rapid review"
- keep only visuals that directly support memorization; omit decorative figures
- produce a note that is optimized for fast recitation before an exam

## Workflow

1. Inspect the PDF first.
   Run `scripts/inspect_pdf.py <book.pdf>` to estimate page count, text coverage, and embedded-image density before writing anything.

2. Decide whether OCR is required.
   If most sampled pages have meaningful text, extract and clean the text directly.
   If the PDF is image-only or nearly image-only, run OCR before content extraction.

3. Preserve the original visual material.
   Run `scripts/extract_pdf_assets.py <book.pdf> --outdir <dir>` to render page previews and extract embedded images.
   Do not assume OCR text is enough; inspect the original pages to keep figures, tables, layouts, and visual explanations.

4. Build the knowledge outline from the book's structure.
   Prefer the table of contents, chapter titles, section titles, theorem/example blocks, and visual groupings over page order alone.
   Merge repetitive prefaces, copyright pages, indexes, and references unless the user explicitly wants them covered.

5. Choose the writing mode from the user's intent.
   Default to knowledge-summary notes, not guide-style notes.
   If the user asks for exam review, memorization, basic recitation, sprint revision, or "memorization only", switch to exam-cram mode.

6. Write the note in Chinese unless the user requests another language.
   Start from `assets/notes-template.tex`.
   Put the best available cover image or first-page cover on the title page.

7. Compile the `.tex` into a final PDF.
   Fix LaTeX issues before delivery.

## OCR Decision Rules

- Prefer native text extraction when the PDF already contains reliable text.
- Trigger OCR when extracted text is missing, mostly garbled, or present on only a small fraction of pages.
- Prefer `ocrmypdf` when available because it preserves the original PDF while adding a text layer.
- If OCR tooling is missing, read `references/tooling.md` and install the minimum dependency needed before continuing.
- Keep both the OCR result and the original PDF when practical so figures can still be checked against the source pages.

## Writing Rules

1. Write the notes in Chinese unless the user explicitly asks for another language.

2. Organize the document with `\section{...}` and `\subsection{...}`.
   Reconstruct the knowledge flow when needed; do not mirror every page mechanically.
   Prefer concept clusters, methods, contrasts, and chapter takeaways over page-by-page narration.

3. Start from `assets/notes-template.tex`.
   Fill the metadata block, including the local cover image path, and replace the body content block with the generated notes.

4. Keep the book's visuals.
   Include figures whenever a diagram, table, page fragment, or formula image materially improves understanding or memorization.
   Do not replace figure-heavy explanations with plain prose if the visual carries meaning.

5. When a mathematical formula appears:
   show it in display math using `$$...$$`
   then immediately follow with a flat list explaining each symbol

6. When code examples appear:
   wrap them in `lstlisting`
   include a descriptive `caption`

7. Use `importantbox`, `knowledgebox`, and `warningbox` only for genuinely high-signal takeaways.
   Keep images outside those boxes.

8. End every major section with a subsection such as `\subsection{Key Points Summary}`.
   Replace that placeholder with Chinese in the final note.
   Use that subsection to compress the section into memorisable knowledge points.
   Add an extended-reading subsection only when worthwhile external references exist.

9. End the document with a final top-level section such as `\section{Final Synthesis}`.
   Replace that placeholder with Chinese in the final note.
   Include the book's closing synthesis when meaningful, plus your own distilled takeaways, cross-links, and a whole-book knowledge map.

10. If exam-cram mode is active:
   use short sentences and dense bullet lists
   prefer definitions, classifications, causes, significance, and measures
   include short-answer templates when the source material supports them
   add one final section that compresses the whole book into a last-minute memorization sheet

11. Avoid guide-style filler.
   Do not spend space on reading advice, publication background, or chapter previews unless they directly help understand the knowledge points.
   Prioritize "what to know", "how to distinguish", "how to apply", and "what is easy to confuse".

## Figure Handling

Select figures by teaching value, not by quota.

- Inspect rendered pages and extracted embedded images together.
- Prefer the highest-quality original figure asset when the PDF contains an embedded image.
- If the book's figure is only visible as part of the page layout, crop or use the page render rather than omitting it.
- Include multiple visuals in one section when the material builds in stages.
- Omit decorative or redundant images.
- Preserve readability of labels, formulas, and table cells.

## Figure Provenance

Whenever the `.tex` references a figure from the book, record its source page on the same page as a bottom footnote.

- Use concrete page numbers such as `source book page 42`.
- If the figure is cropped from a page render, the footnote still cites the original source page.
- Keep the figure and provenance footnote on the same page when possible.

## Scripts

- `scripts/inspect_pdf.py`
  Inspect a PDF and report whether OCR is likely required.

- `scripts/extract_pdf_assets.py`
  Render pages and extract embedded images for figure selection.

- `scripts/run_ocr.py`
  Wrapper around `ocrmypdf` with a clear fallback error when OCR tooling is unavailable.

Read `references/tooling.md` only when you need installation or dependency guidance.

## Delivery

Deliver all of the following:

- the final `.tex` file
- the cover image used on the front page
- any extracted or cropped figure assets referenced by the document
- the compiled PDF
- optional inspection or asset manifests when they help the user audit the workflow
