---
title: "Nine Reviewer Disciplines: Table (1)"
description: "Shared rules; disciplines Architecture-Performance."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use to find a finding's owning specialist."
---

# The Nine Reviewer Disciplines (table part 1: Architecture - Performance)

Every specialist inherits the monolith's hard rules verbatim — numeric confidence 0-100
with findings below 80 hard-dropped, CRITICAL/HIGH/MEDIUM/LOW severity, every finding
line-anchored with `file:line` plus a link to the specific `repo-governance/` rule it cites,
anti-sycophantic framing, a scope guard limited to the PR's own declared plan/issue scope, and
untrusted-input filtering of PR body/comment/linked-issue text. What differs per specialist is its
**owned discipline** and the **scope it explicitly routes elsewhere** rather than raising itself:

| Discipline                     | Specialist agent               | Owns (in-charter)                                                                                                       | NOT its job (routes to)                                                                                                                 |
| ------------------------------ | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Architecture                   | `pr-review-architecture-maker` | New tradeoffs, module boundaries, reversibility, blast radius, quality-attribute effects, novel dependencies            | Existing-rule layering violations → governance; domain-scenario gaps → logic                                                            |
| Business-logic / correctness   | `pr-review-logic-maker`        | Behavior vs. domain intent + Gherkin acceptance-criteria conformance across edge/error cases                            | Error-handling _shape_ rules → governance; should-this-boundary-exist → architecture                                                    |
| Governance / rules-conformance | `pr-review-governance-maker`   | Mechanical conformance to already-documented `repo-governance/` conventions, naming/structure, ADRs, spec-file presence | Whether a new rule should exist → architecture; scenario completeness → logic; instruction-decay (stale instruction docs) → instruction |
| Security                       | `pr-review-security-maker`     | Secrets in diffs, injection, untrusted-input handling, git-fixture isolation, unsafe git/FS operations                  | Non-security convention text → governance                                                                                               |
| CI-gaming / test-integrity     | `pr-review-integrity-maker`    | CI-gaming (weakened/skipped/narrowed tests, coverage-gaming), missing regression tests (regression-test-mandate)        | Whether the behavior is correct → logic                                                                                                 |

**Continued in** [Nine Reviewer Disciplines: Table (2)](./the-nine-reviewer-disciplines-table-part-2.md) — Performance through Type-soundness, plus the scout/synthesis roles.
