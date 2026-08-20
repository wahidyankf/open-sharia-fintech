---
name: docs-fixing-factual-accuracy
description: Complete methodology for re-validating and applying docs-checker factual-accuracy findings without web access — the trust model, domain-specific confidence examples, per-finding-type re-validation guidance, fix application patterns, the fix report format, and convergence safeguards. Backs the docs-fixer agent.
---

# Documentation: Fixing Factual Accuracy Findings

Methodology for re-validating `docs-checker` audit findings and applying only HIGH-confidence,
objective fixes — without independent web access, trusting the checker's documented verification.

## Reference Modules

1. [Confidence Assessment and Mode Handling](reference/confidence-and-mode-handling.md) — the
   quick-summary workflow, domain-specific HIGH/MEDIUM/FALSE_POSITIVE examples.
2. [Trust Model and Re-Validation Guidelines](reference/trust-model-and-revalidation.md) — why
   this agent has no web tools, how it re-validates without one, and per-finding-type re-validation
   guidance (command syntax, versions, feature existence, code examples, contradictions, outdated
   info).
3. [Fix Patterns and Report Format](reference/fix-patterns-and-report-format.md) — the six fix
   application patterns and the full fix-report markdown template.
4. [Tools, Best Practices, and Safeguards](reference/tools-practices-safeguards.md) — tool usage,
   best practices, and convergence safeguards (changed-files capture, false-positive persistence,
   self-verification).

## Core Principles

- **Never trust checker findings blindly** — always re-validate before applying.
- **Objective errors only get HIGH confidence** — everything else is MEDIUM (manual review) or
  FALSE_POSITIVE.
- **Checker verifies, fixer applies** — no independent web re-fetching; when in doubt, downgrade
  confidence rather than guess.

## Related Skills

- `repo-applying-maker-checker-fixer` — the generic maker-checker-fixer pattern, mode-parameter
  handling, and report discovery.
- `repo-assessing-criticality-confidence` — the generic criticality × confidence priority matrix.
- `repo-generating-validation-reports` — report file naming and UUID-chain conventions.
