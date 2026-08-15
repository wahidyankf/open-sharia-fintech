---
title: "Governance README Completeness Convention"
description: Two-gate README index enforcement — orphan/ghost link detection plus missing/unannotated completeness checks
when_to_use: Use when a directory's README.md fails an orphan, ghost, missing, or unannotated finding.
category: explanation
subcategory: conventions
tags:
  - readme
  - governance
  - rhino-cli
  - index
created: 2026-08-15
---

# Governance README Completeness Convention

Every directory that needs an index — one with a sibling `.md` file besides `README.md`, or a
subdirectory carrying its own `README.md` — must have one, and that index must link every such
sibling with a derived annotation. `rhino-cli governance readme-index validate` enforces this via
two separately-registered `gates:` entries that invoke the **same** underlying binary
(`governance readme-index validate`) with different `args`.

## The Two Gates

| Gate id                          | Finding kinds            | Scan scope (`--paths`)                                                                                              | Armed                                             |
| -------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `governance-readme-index`        | `orphan`, `ghost`        | `DEFAULT_PATHS`: `repo-governance/`, `.claude/agents/`, `.claude/skills/`, `docs/explanation/software-engineering/` | Continuously, since Phase 1                       |
| `governance-readme-completeness` | `missing`, `unannotated` | `repo-governance/`, `.claude/`, `.codex/`, `.pi/`                                                                   | Phase 9 (`ose-public`) / Phase 16 (`ose-private`) |

## Finding Kinds

- `orphan` — a sibling `.md` file or subdirectory README exists but is not linked from the index.
- `ghost` — the index links a target that does not exist on disk.
- `missing` — a directory needs an index (per the rule above) but has none.
- `unannotated` — the index links a target with no `- [<title>](<path>) — <description>
<when_to_use>` annotation on that line (an em-dash or `--` followed by non-whitespace text).

## Remediation

Run `rhino-cli governance readme-index generate <dir>` to scaffold a compliant `README.md` for a
directory reported `missing`. For `orphan`/`ghost`/`unannotated`, hand-edit the index: add the
missing link, remove the dangling one, or append `— <description>` derived from the target's own
frontmatter `description` (and `when_to_use` where the target carries one). An annotation that
merely repeats text already stated in the surrounding sentence or an adjacent table column adds no
navigational value — write it to convey information the reader doesn't already have.

## Enforcement Points

Both gates run at pre-push (changed-path gated) and in the PR quality gate (CI). Neither runs at
pre-commit — a whole-tree scan on every commit buys no additional coverage over pre-push/CI.

## Updating Scope

Edit the `args.paths`/`args.exclude`/`trigger` lists on the relevant `gates:` entry in
`repo-config.yml` and record the rationale as a YAML comment.
