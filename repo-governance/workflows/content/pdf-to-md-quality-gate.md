---
name: pdf-to-md-quality-gate
title: "pdf-to-md-quality-gate"
description: Converts a PDF to verbatim Markdown and validates fidelity via Maker-Checker-Fixer until convergence.
when_to_use: Use when converting a PDF to Markdown, or revalidating an existing PDF-derived Markdown file.
goal: Convert a PDF file to verbatim Markdown and validate conversion fidelity iteratively until zero findings achieved on two consecutive checks
termination: "Zero findings on two consecutive validations (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: pdf-file
    type: string
    description: Path to source PDF file (source of truth)
    required: true
  - name: md-file
    type: string
    description: Path to output Markdown file; default is same directory and filename as pdf-file with .md extension
    required: false
  - name: force-remake
    type: boolean
    description: Re-run maker even if Markdown file already exists
    required: false
    default: false
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: Minimum check-fix cycles before allowing zero-finding termination (prevents premature success)
    required: false
  - name: max-iterations
    type: number
    description: Maximum check-fix cycles to prevent infinite loops
    required: false
    default: 7
  - name: max-concurrency
    type: number
    description: "N+1 background-agent cap. Raise only for independent work with capacity and budget; lower under pressure; never self-promote."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final validation status
  - name: lifecycle-status
    type: enum
    values: [verified, pending, not-applicable]
    description: Lifecycle evidence state, separate from final-status
  - name: iterations-completed
    type: number
    description: Number of check-fix cycles executed
  - name: pdf-to-md-report
    type: file
    pattern: generated-reports/pdf-to-md__*__audit.md
    description: Final fidelity validation audit report
  - name: execution-scope
    type: string
    description: Scope identifier for UUID chain tracking (default "pdf-to-md")
    required: false
---

# PDF-to-Markdown Quality Gate Workflow

**Purpose**: Convert a PDF to a complete, verbatim Markdown representation, then validate fidelity
iteratively via the **Maker-Checker-Fixer pattern** until all issues resolve. The Markdown becomes
a cross-reference source-of-truth proxy for the original PDF.

**When to use**: converting a new PDF, revalidating after manual Markdown edits, or validating an
existing conversion before treating it as a reference source.

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
