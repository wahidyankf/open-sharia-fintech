# 📄 File Naming Convention Rework (WS-B)

## Context

WS-B was **declared but deliberately unspecified** in
[`repo-rules-sweep`](../../done/2026-08-18__repo-rules-sweep/README.md): that plan touched
`file-naming.md` only enough to remove the contradiction WS-A created, and left the broader rework to
be specified "only after WS-A's Knowledge Capture records what is still wrong".

That record now exists — entries 6, 7, and 8 of
[`repo-rules-sweep/learnings.md`](../../done/2026-08-18__repo-rules-sweep/learnings.md). This plan is WS-B,
specified from it.

## The Problem

Two conventions now govern governed filenames — `file-naming.md` and
`ordinal-filename-prefixes.md` — and executing a 2000-file sweep across two repositories exposed
that both misstate what is actually enforced.

**`file-naming.md` names two exemptions; the gate has eleven.**
`md naming validate` hard-codes nine exempt basenames (`README.md`, `SKILL.md`, `AGENTS.md`,
`CLAUDE.md`, `_index.md`, `CONTRIBUTING.md`, `LICENSING-NOTICE.md`, `ROADMAP.md`, `SECURITY.md`) and
`repo-config.yml` adds two more globs (`*__linkedin__*.md`, plus a redundant second statement of
`CONTRIBUTING.md`). The convention names `README.md` and `SKILL.md`. `AGENTS.md` and `CLAUDE.md` are
among the most-edited files in the repository and appear in no exception clause.

**One exemption contradicts the rule in writing.** The rule says "no underscores in the basename";
`_index.md` is exempt because Hugo requires it, and no document says so. A reader following the
convention concludes every `apps/*-www` content section is in violation.

**The scope clause is unfalsifiable, and the code leans on it.** The convention governs
"`docs/`, `repo-governance/`, and similar locations". `naming.rs`'s own doc comment quotes that
phrase back as justification for its exemptions. The gate's real scope is every tracked `.md` minus
the exempt list.

**Four of six governed extensions are unenforced.** The rule lists `.md`, `.png`, `.svg`, `.mmd`,
`.excalidraw`, `.drawio`; the validator's first act is to skip anything not ending in `.md`.

**The ordinal convention contradicts its own worked example.** `ordinal-filename-prefixes.md` states
that an ordinal is kept only when it is "that step's own number", then its table keeps the ordinal on
`02-step-1-and-2-maker-and-checker.md` while that row's own verdict says the two numbering systems
disagree. The reconciling range clause sits below the table and is never applied to the row.

**The ordinal rule has no verdict for name collisions.** `ose-private` holds 18 groups (40 files)
whose basenames were truncated to a fixed width by an earlier word-budget split, leaving pairs that
differ **only** by ordinal. They are not steps, so the keep-clause does not apply; stripping collides,
so the strip-clause cannot be applied either. Those 40 files kept their ordinals as the sole
documented deviation between the two repositories' sweeps.

## Workstreams

| ID    | Workstream                                                      | Status    |
| ----- | --------------------------------------------------------------- | --------- |
| WS-B1 | Reconcile `file-naming.md` with the enforced rule               | Specified |
| WS-B2 | Repair the ordinal convention's self-contradiction              | Specified |
| WS-B3 | State a verdict for truncated-stem collisions, and prevent them | Specified |

## Scope

**Repositories**: `ose-public` and `ose-private`. Both carry both conventions; both were created or
edited by `repo-rules-sweep`.

**Trees in scope**: `repo-governance/conventions/structure/`, the rules-machinery agents and skills
that restate either rule, `repo-config.yml`'s `md-naming` args, and — for WS-B3 only —
the word-budget remediation tooling that produces truncated names.

**Out of scope**: renaming any existing file. This plan changes what the rules **say** and, in WS-B3,
what the split tool **emits**; a corrective sweep of the 40 collision files is separate work that
this plan's WS-B3 verdict must precede.

## Approach Summary

Derive every claim from the enforcing code and the gate registry before writing prose — the same
method that produced the defect list. Then propagate through every surface that restates the rule, per
[Iron Rule 3](../../../repo-governance/workflows/plan/plan-execution/iron-rules-1-5.md): fix the class,
not the sites a finding names.

WS-B3 is the only workstream that touches code, and only the emitter — the rule verdict it needs
comes first.

## Documents

- [brd.md](./brd.md) — why the drift matters.
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — the derivation method and the per-defect design.
- [delivery.md](./delivery.md) — the phase-by-phase execution checklist.
