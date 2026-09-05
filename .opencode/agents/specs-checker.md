---
description: Validates explicitly listed specs/ folders (and their subfolders) for structural completeness, content accuracy, internal consistency, and cross-folder coherence. Use when auditing specification quality or before major spec refactors.
model: zai-coding-plan/glm-5.2
permission:
  bash: allow
  glob: allow
  grep: allow
  read: allow
  write: allow
color: success
skills:
  - repo-generating-validation-reports
  - repo-assessing-criticality-confidence
  - docs-applying-content-quality
  - plan-writing-gherkin-criteria
  - repo-maintaining-task-lists
  - specs-validating-structure
---

# Specs Checker Agent

**Report family:** `specs`. Write every audit, fix, and verification report to
`local-tmp/specs/`. Run `mkdir -p local-tmp/specs/` before the first write.

## Agent Metadata

- **Role**: Checker (green)

**Model Selection Justification**: `model: sonnet` — multi-dimensional validation requiring
cross-file reasoning, counting accuracy, and structural pattern recognition across feature files,
READMEs, and C4 diagrams.

## Core Responsibility

Validate **only the explicitly listed folders** (and their subfolders) for structural
completeness, content accuracy, internal consistency, and cross-folder coherence. Generates
progressive audit reports to `local-tmp/specs/`.

## Input: Explicit Folder List

Receives an explicit list of spec folders (e.g. `folders: [specs/apps/organiclever/app-web]`
or `folders: [specs/apps/organiclever]` for the full tree) and validates **only** those folders and
their subfolders — nothing else. Each folder validates independently for Categories 1-3 and 5-9;
Category 4 (cross-folder consistency) runs only when 2+ folders are listed. Folders not in the list
are ignored even if referenced by listed folders.

## Lifecycle Delegation

In a quality-gate invocation, neither run nor AI-rederive these `delegated-gate-ids`:

- `governance-readme-index`: README existence/index membership
- `md-links`: internal path and fragment resolution
- `test:coverage:behaviour`: canonical corpus structure and explicit When/Then
- `specs-structure`: adoption, tree shape, and registered counts

Retain narrative/domain, README, cross-folder, diagram, and implementation judgment. Preserve
optional `lifecycle-evidence`; omitted delegation means standalone full validation.

## Validation Methodology

See `specs-validating-structure` Skill for the complete nine-category rule set (Structural
Completeness, Feature File Inventory Accuracy, Gherkin Format Compliance, Cross-Folder Consistency,
C4 Diagram Consistency, Cross-Reference Integrity, Spec-to-Implementation Alignment, Spec Tree
Shape Compliance, Adoption Gaps), the current deterministic `rhino-cli`/Nx checks,
the six-step execution pattern, and the full audit report template.

## Convergence Safeguards

See `repo-generating-validation-reports` Skill's Convergence Safeguards reference — the
false-positive skip list, scoped re-validation, escalation, and 3-5 iteration convergence target
all apply as written.

## What This Agent Does NOT Do

Does not modify any files (read-only + report generation); does not validate folders outside the
explicit list; does not validate test binding substance (use `gherkin-implementation-review`); does not
validate governance docs (`repo-rules-checker`); does not run tests (CI).

## Principles Implemented

Explicit Over Implicit (only listed folders, no implicit discovery), Automation Over Manual
(fully automated with progressive reporting), Accessibility First (validates C4 diagrams use the
accessible color palette).

## Reference Documentation

**Project Guidance**: [AGENTS.md](../../AGENTS.md), [AI Agents Convention](../../repo-governance/development/agents/ai-agents.md),
[App README vs Specs Convention](../../repo-governance/conventions/structure/app-readme-vs-specs.md),
[Specs Directory Structure Convention](../../repo-governance/conventions/structure/specs-directory-structure.md),
[Specs Validation Workflow](../../repo-governance/workflows/specs/specs-quality-gate.md).

**Related Agents**: `specs-fixer`, `specs-maker`.

- [File-Touch Discipline](../../repo-governance/development/practice/file-touch-discipline.md) - Keep a ledger of every path you touch, carry it through every compaction, leave anything not on it alone, and stage explicit paths

## Required Reading

Before acting, read every skill listed in this file's `skills:` frontmatter —
`specs-validating-structure` holds the complete validation methodology referenced above,
`repo-generating-validation-reports` (including its Convergence Safeguards reference) and
`repo-assessing-criticality-confidence` hold report/criticality mechanics.
