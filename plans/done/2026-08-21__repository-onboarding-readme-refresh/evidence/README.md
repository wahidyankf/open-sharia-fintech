# Evidence Index

Sanitized index of what this plan produced and where each result is recorded. No raw tool output,
no environment data, no authentication state, and no local filesystem path appears here or in any
file it indexes.

## Pull requests

| PR  | Unit                       | Outcome |
| --- | -------------------------- | ------- |
| 236 | Plan documents             | Merged  |
| 237 | Documentation contract     | Merged  |
| 238 | Reader-facing refresh      | Merged  |
| 239 | Correction iteration `@01` | Merged  |
| 240 | Correction iteration `@02` | Merged  |

## Repository metadata

Phase 4 compared the live GitHub About fields against the contract recorded in Phase 2 and verified
exact set equality on description, homepage, and the topic array. The prior field values were
captured before any write so the change was reversible; no restore was needed.

## Local journeys

Both journeys followed the documented onboarding path in a disposable environment and reached the
product landing page.

| Journey  | Environment                          | Outcome |
| -------- | ------------------------------------ | ------- |
| Phase 5A | macOS, temporary clone               | Passed  |
| Phase 5B | `ubuntu:24.04`, disposable container | Passed  |

Each journey stopped its dev process and removed its environment. Phase 5B additionally re-ran and
diffed four Docker baseline listings to prove it left no image, container, volume, or network
behind.

## Captured files

Twelve files: nine PNG viewport captures and three text transcripts.

| File pattern                                | What it shows                                   |
| ------------------------------------------- | ----------------------------------------------- |
| `phase-5a-ose-www-landing-en-<width>px.png` | macOS landing page at three viewport widths     |
| `phase-5b-ose-www-landing-en-<width>px.png` | Container landing page at the same three widths |
| `phase-6-ose-www-landing-en-<width>px.png`  | Documented-breakpoint coverage capture          |
| `phase-5a-ose-www-curl.txt`                 | macOS loopback response summary                 |
| `phase-5b-ose-www-curl.txt`                 | Container response summary                      |
| `phase-6-breakpoint-coverage.txt`           | Per-breakpoint overflow check                   |

The captures are viewport-only: no window chrome, terminal, URL bar, or filesystem path is visible.
A byte-level scan confirms none of the nine PNGs carries a `tEXt`, `iTXt`, `zTXt`, or `eXIf`
metadata chunk. All three 768px captures are one byte-identical file — same renderer, same viewport,
identical response body.

## Quality gates

Every repository-authoritative gate was run against merged `main` and passed: Markdown formatting
and linting, link validation at its registered scope, README index validation, harness binding
generation and sync, the `rhino-cli` parity manifest, and both deterministic secret gates. An
independent semantic sensitivity review returned zero findings at any severity.

## Where the detail lives

- `../delivery.md` — every task, its acceptance, and its recorded outcome
- `../artifacts/execution-record-contract.md` — Phases 0–2
- `../artifacts/execution-record-public.md` — Phase 3
- `../artifacts/execution-record-fixes.md` — Phases 6 and its `@01`/`@02` iterations
- `../artifacts/reader-doc-disposition-ose-public.md` — per-document disposition ledger
