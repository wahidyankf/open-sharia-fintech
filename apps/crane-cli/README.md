# crane-cli

Crane helps turn PDFs into dependable Markdown evidence. It is a local F# command-line tool for
checking extraction quality, headings, tables, figures, OCR, and report inputs in a repeatable way.
🪶

## Start with the command help

```bash
npm exec nx -- run crane-cli:run -- --help
```

Run `npm exec nx -- run crane-cli:run -- <command> --help` to explore a specific operation. The main
groups are `pdf`, `text`, `heading`, `nesting`, `table`, `figure`, `mermaid`, `ocr`, `report`,
`skiplist`, and `check-all`.

## Local prerequisites

Most checks run with the repository toolchain. OCR additionally needs Tesseract and Poppler:

| Platform      | Install command                                                                      |
| ------------- | ------------------------------------------------------------------------------------ |
| macOS         | `brew install tesseract poppler`                                                     |
| Ubuntu/Debian | `sudo apt-get install tesseract-ocr libleptonica-dev libtesseract-dev poppler-utils` |

Point `TESSDATA_PREFIX` at your local Tesseract data directory when your installation needs it.

## Build and verify

```bash
npm exec nx -- run crane-cli:build
npm exec nx -- run crane-cli:test:quick
npm exec nx -- run crane-cli:test:integration
```

The executable is written to `apps/crane-cli/dist/` by the build target. Its behavior specifications
live in [the Crane Gherkin suite](../../specs/apps/crane/cli/behaviors/README.md).

## Code map

- `src/Core/` — domain types, ports, and pure checking logic
- `src/Adapters/In/` — command-line parsing and dispatch
- `src/Adapters/Out/` — PDF and OCR integrations
- `Program.fs` — local composition root

The shape is deliberately ports-and-adapters: the checking logic can stay understandable while file
and OCR integrations remain at the edge.
