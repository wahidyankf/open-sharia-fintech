---
name: plan-validating-quality
description: Full validation methodology for project plans — structure, requirements (BRD/PRD), technical documentation, delivery-checklist executability, and 21 numbered validation rules (operational readiness, manual assertions, worktree/delivery-mode compliance, anti-hallucination, phase gates, specs/UI/learning coverage, Vercel MCP capability). Used by plan-checker.
when_to_use: When validating a project plan before execution, or extending/auditing the plan-checker agent's methodology.
---

# Validating Plan Quality

Full methodology for `plan-checker`: what "complete, clear, and executable" means for a project plan,
across structure, requirements, technical docs, delivery-checklist granularity, and 21 numbered
validation rules layered on top of the base five validation-scope sections.

## Reference Modules

- `reference/01-structure-requirements-techdocs.md` — Validation Scope 1-3: folder/file structure,
  BRD/PRD content placement, technical documentation and the File-Impact tree HARD RULE.
- `reference/02-delivery-checklist-and-pr-authorization.md` — Validation Scope 4-5: the full HARD
  RULE summary layer for delivery checklists, the PR Step Authorization Check (with detection
  scripts), No PR Outside a Declared Delivery Boundary, granularity standard, and consistency
  validation.
- `reference/03-workflow-and-factual-accuracy.md` — the Step 0-7 execution sequence (false-positive
  skip list, re-validation mode, codebase inspection) and Factual Accuracy Validation (Step 4b).
- `reference/04-operational-readiness-through-worktree.md` — rules 8-11: Operational Readiness (5b),
  Manual Behavioral Assertion (5c), Worktree Specification (5d), Execution-Grade Clarity (5e).
- `reference/05-anti-hallucination-through-phasegate.md` — rules 12-15: Anti-Hallucination Scan (5f),
  Harness-Neutrality Scan (5g), Executor-Tag Validation (5h), Phase-Gate & Natural-Pause (5i).
- `reference/06-specs-ui-knowledge-capture.md` — rules 16-18: Specs & Gherkin Coverage (5j) plus the
  Regression Test Mandate, UI-Design-Funnel Completeness (5k), Knowledge Capture Phase Presence (5l).
- `reference/07-delivery-mode-syllabus-vercel.md` — rules 19-21: Delivery Mode Validation (5m),
  Learning-Bearing Syllabus Completeness (5n), Vercel MCP Capability Declaration (5o).

## Core Principles

**Every rule states its own criticality** (CRITICAL/HIGH/MEDIUM/LOW) — never freelance a severity not
listed in the owning reference module. **Falsifiable both ways**: every detection command's acceptance
criterion must be checked against both the pre-violation and post-violation state before trusting it.
**Conditional rules skip cleanly**: Harness-Neutrality (13), Learning-Bearing Syllabus (20), and Vercel
MCP (21) are scope-gated — record the exemption explicitly rather than silently omitting the check.

## Related

`repo-generating-validation-reports` (report format, Convergence Safeguards), `repo-applying-maker-checker-fixer`
(workflow shape), `docs-validating-factual-accuracy` (Step 4b methodology), `plan-writing-gherkin-criteria`
(Gherkin authoring rules this validates against), `plan-creating-project-plans` (the authoring-side
counterpart plan-checker validates against).
