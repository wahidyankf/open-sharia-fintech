---
title: "PDF to Markdown"
description: "Agents that convert PDF sources to verbatim Markdown and validate or fix the conversion."
---

# PDF to Markdown

- [Pdf To Md Checker](./pdf-to-md-checker.md) — Validates that a Markdown file is a verbatim, complete representation of its source PDF. Checks for missing sections, incorrect text, table integrity, OCR quality, Mermaid validity, and figure coverage. Use when verifying PDF-to-Markdown conversion fidelity before cross-referencing.
- [Pdf To Md Fixer](./pdf-to-md-fixer.md) — Applies validated fixes from pdf-to-md-checker audit reports. Re-validates each finding before applying. Fixes missing sections (re-extracts from PDF), incorrect text, wrong table data, invalid Mermaid syntax, and missing figure placeholders. Use after reviewing pdf-to-md-checker output.
- [Pdf To Md Maker](./pdf-to-md-maker.md) — Converts PDF files to verbatim Markdown representations. Handles text-based PDFs via pdftotext, image-only PDFs via OCR (tesseract), converts diagrams to Mermaid format, and processes arbitrarily large files in 50-page chunks. By default outputs to same directory and filename as PDF with .md extension. Use when converting a PDF to Markdown for cross-referencing or archival.
