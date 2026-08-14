---
title: "Markdown Quality Gates"
description: "The markdown-specific quality gates and their commands."
category: explanation
subcategory: development
tags:
  - validation
  - consistency
  - bash
  - awk
  - frontmatter
  - automation
created: 2025-12-14
when_to_use: "Use when locating a markdown quality gate's command or exclusions."
---

# Markdown Quality Gates

Three automated markdown validators run on every commit and in CI. Per-file validators (mermaid,
heading-hierarchy) run via lint-staged; the repo-wide link validator (`md links validate`) runs as
the `md-links` gate job in `pr-quality-gate.yml`:

## 1. Mermaid Diagram Validation

**Command**: `npx nx run rhino-cli:mermaid:validation`

Repo-wide scan: the Nx target runs `md validate mermaid --max-depth=4 --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content` (plus the standardized noise-skip set: `node_modules`, `dist`, `target`, `.next`, `coverage`, `generated-reports`, `local-temp`, `archived`, `worktrees`, `.terraform`, `generated-contracts`, `.nx`, `.git`). Checks: maximum horizontal width (4 nodes per rank), label line length (≤ 30 chars), single diagram per fenced block, valid syntax. Diagram types covered: `flowchart`/`graph` (all directions) and `stateDiagram-v2`/`stateDiagram` (v1) — state node count contributes to width; state display names and transition edge labels are subject to the ≤ 30-char limit. The `--exclude` flag is repeatable; pass additional prefixes to suppress noise in project-specific runs.

**Gate locations**: Pre-commit (staged `.md` files only, via lint-staged). Not at pre-push. Not in
a standalone CI workflow (markdown validation is folded into lint-staged and `pr-quality-gate.yml`).

## 2. Markdown Link Validation

**Command**: `npx nx run rhino-cli:links:validation`

Full-repo link scan (same standardized noise-skip set as `mermaid:validation`). Validates all relative `[text](path.md)` links resolve to existing files. Also validates `#fragment` anchor references using the GitHub slug algorithm — underscores and Unicode letters/digits are kept, spaces map to hyphens, duplicates receive `-1`, `-2`, … suffixes (verified against the `github-slugger` v2 reference implementation). A fragment with no matching heading emits a `broken-anchor` finding.

**Gate locations**: Pre-commit (staged `.md` files only, link step) + `md-links` gate job in
`pr-quality-gate.yml`. Not at pre-push.

## 3. Heading Hierarchy Validation

**Command**: `npx nx run rhino-cli:headings:hierarchy-validation`

Validates heading nesting on a prose allowlist (default-deny): `docs/`, `repo-governance/`, `plans/` (excluding `plans/done/`), `specs/`, root `*.md`, `apps/*/README.md`, `libs/*/README.md`, `apps/*/docs/**`, `libs/*/docs/**`. All other paths (including `.claude/**`, `apps/ayokoding-www/content/`, `apps/ose-www/content/`, `plans/done/`) are skipped.

**Gate locations**: Pre-commit (staged `.md` files within the prose allowlist, via lint-staged). Not
at pre-push. Not in a standalone CI workflow (folded into lint-staged and `pr-quality-gate.yml`).

## CI Enforcement

The standalone `markdown-validate.yml` workflow has been deleted. Markdown validation now runs via
lint-staged (per-file: mermaid, heading-hierarchy, markdownlint) and the `md-links` gate job in
`pr-quality-gate.yml` (repo-wide link validation on every `push` and `pull_request` targeting `main`).
