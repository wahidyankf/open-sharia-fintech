---
description: Converts a PDF to verbatim Markdown and validates fidelity via Maker-Checker-Fixer until convergence.
when_to_use: Use when converting a PDF to Markdown, or revalidating an existing PDF-derived Markdown file.
---

# PDF-to-Markdown Quality Gate Workflow

**Purpose**: Convert a PDF to a complete, verbatim Markdown representation, then validate fidelity
iteratively via the **Maker-Checker-Fixer pattern** until all issues resolve. The Markdown becomes
a cross-reference source-of-truth proxy for the original PDF.

**When to use**: converting a new PDF, revalidating after manual Markdown edits, or validating an
existing conversion before treating it as a reference source.

## Goal and Termination

**Goal**: Convert a PDF file to verbatim Markdown and validate conversion fidelity iteratively until zero findings achieved on two consecutive checks

**Termination**: Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)

## Inputs

- **`pdf-file`** (string, required) — Path to source PDF file (source of truth)
- **`md-file`** (string, optional) — Path to output Markdown file; default is same directory and filename as pdf-file with .md extension
- **`force-remake`** (boolean, optional, default `false`) — Re-run maker even if Markdown file already exists
- **`mode`** (enum: lax, normal, strict, ocd, optional, default `strict`) — Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)
- **`min-iterations`** (number, optional) — Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
- **`max-iterations`** (number, optional, default `7`) — Maximum check-fix cycles to prevent infinite loops
- **`max-concurrency`** (number, optional, default `3`) — N+1 background-agent cap. Raise only for independent work with capacity and budget; lower under pressure; never self-promote.

## Outputs

- **`final-status`** (enum: pass, partial, fail) — Final validation status
- **`lifecycle-status`** (enum: verified, pending, not-applicable) — Lifecycle evidence state, separate from final-status
- **`iterations-completed`** (number) — Number of check-fix cycles executed
- **`pdf-to-md-report`** (file, pattern `local-tmp/pdf-to-md/pdf-to-md__*__audit.md`) — Final fidelity validation audit report
- **`execution-scope`** (string) — Scope identifier for UUID chain tracking (default "pdf-to-md")

## Contents

- [Lifecycle validation ownership](../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md) — shared Step 0.
- [Execution Mode](./pdf-to-md-quality-gate/execution-mode.md) — delegation vs. manual mode.
- [Workflow Overview](./pdf-to-md-quality-gate/workflow-overview.md) — flow diagram.

### Steps

- [Step 1: Generate Markdown](./pdf-to-md-quality-gate/step-1-generate-markdown.md) — maker.
- [Step 2: Validate Fidelity](./pdf-to-md-quality-gate/step-2-validate-fidelity.md) — checker.
- [Step 3: Check for Findings](./pdf-to-md-quality-gate/step-3-check-for-findings.md) — threshold.
- [Step 4: Apply Fixes](./pdf-to-md-quality-gate/step-4-apply-fixes.md) — fixer, downgrade rules.
- [Step 5: Re-validate](./pdf-to-md-quality-gate/step-5-revalidate.md) — scoped re-check.
- [Step 6: Iteration Control](./pdf-to-md-quality-gate/step-6-iteration-control.md) — loop logic.
- [Step 7: Finalization](./pdf-to-md-quality-gate/step-7-finalization.md) — final status.

### Criteria and Examples

- [Termination Criteria](./pdf-to-md-quality-gate/termination-criteria.md) — pass/partial/fail.
- [Example Usage](./pdf-to-md-quality-gate/example-usage.md) — invocation scenarios.
- [Iteration Example](./pdf-to-md-quality-gate/iteration-example.md) — multi-iteration trace.

### Safety and Reference

- [Safety Features](./pdf-to-md-quality-gate/safety-features.md) — convergence safeguards.
- [Tool Dependencies](./pdf-to-md-quality-gate/tool-dependencies.md) — crane-cli, tesseract, jq.
- [Validation Dimensions](./pdf-to-md-quality-gate/validation-dimensions-summary.md) — dimension table.
- [Principles Respected](./pdf-to-md-quality-gate/principles-implemented-respected.md) — governance.
- [Conventions Respected](./pdf-to-md-quality-gate/conventions-implemented-respected.md) — naming/linking.
- [Related Workflows](./pdf-to-md-quality-gate/related-workflows.md) — composable workflows.
- [Related Agents](./pdf-to-md-quality-gate/related-agents.md) — maker/checker/fixer.
