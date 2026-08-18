---
name: repo-rules-fixing
description: Mechanics for repo-rules-fixer — applying validated fixes from a repo-rules-checker audit report across agent-skill duplication, skills coverage gaps, rules governance, licensing convention, and software-documentation findings.
when_to_use: When implementing or maintaining repo-rules-fixer, or any agent that applies validated fixes from a repository-wide rules audit report.
---

# Repository Rules Fixing Protocol

## Overview

`repo-rules-fixer` reads a `repo-rules-checker` audit report and applies fixes across six
finding categories. This skill holds the shared edit-safety discipline, the fix procedures per
category, and the re-validation/carry-forward mechanics — kept in ONE place because the source
agent had this content duplicated 2-3x across its own sections.

## Reference Modules

- [verification-and-edit-discipline.md](reference/verification-and-edit-discipline.md) —
  post-fix verification, Python-for-multi-line-edits, confidence re-validation, changed-file
  capture, FALSE_POSITIVE carry-forward, mode handling
- [agent-skill-and-coverage-fixes.md](reference/agent-skill-and-coverage-fixes.md) —
  agent-Skill duplication removal, Skills coverage gap remediation
- [governance-and-licensing-fixes.md](reference/governance-and-licensing-fixes.md) —
  rules governance fixes (contradictions/inaccuracies/inconsistencies/traceability/layer
  coherence), licensing convention fixes
- [software-documentation-fixes.md](reference/software-documentation-fixes.md) — the 8
  software-documentation sub-patterns, re-validation strategy, execution order, tool selection

## Core Principles

- **Post-fix verification is mandatory, not optional.** `sed -i` exits 0 even when its pattern
  matched nothing — a silent no-op that has produced garbled headings in prior iterations. Every
  fix is grepped for after applying, never trusted from exit code alone.
- **Python, not sed, for multi-line agent file edits.** `sed` is line-oriented and silently fails
  on patterns spanning multiple lines; use the Python heredoc pattern in reference module 01.
- **Re-validate before every fix.** The checker's finding may already be stale — re-read the
  current file state before applying, never apply blind from the report text.
- **FALSE_POSITIVE carry-forward is mandatory.** Every skipped finding is persisted with a stable
  key so re-runs don't re-flag it.

## Related Agents

`repo-rules-checker` (produces the audit report this agent consumes), `repo-rules-maker` (creates
new rules — different lifecycle stage).
