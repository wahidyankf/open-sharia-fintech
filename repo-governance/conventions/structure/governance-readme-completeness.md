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

**Every directory carries a literal `README.md` — no exception.** A sibling `<dir-name>.md`
progressive-disclosure parent no longer excuses one; the former split-directory exemption is
removed. That index must link every sibling `.md` file and every subdirectory. Two
separately-registered `gates:` entries enforce it, both invoking the same
`governance readme-index validate` binary with different `args`.

A `<dir-name>.md` parent stays audited as a second index over the same contents; linking it
satisfies the subdirectory requirement — no index carries two links to one target.

## The Two Gates

| Gate id                          | Finding kinds                | Scan scope (`--paths`)                            | Armed                                             |
| -------------------------------- | ---------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| `governance-readme-index`        | `missing`, `orphan`, `ghost` | `docs/`, `repo-governance/`, `specs/`, `.claude/` | Continuous since Phase 1                          |
| `governance-readme-completeness` | `missing`, `unannotated`     | `repo-governance/`, `.claude/`, `.codex/`, `.pi/` | Phase 9 (`ose-public`) / Phase 16 (`ose-private`) |

Structural enforcement covers every content tree. Annotation enforcement stays scoped to trees that
can satisfy it: `docs/` indexes are partly hand-designed tables and `specs/` targets carry no
frontmatter, so no annotation is derivable. Raising those two is tracked separately.

Generated mirrors (`.opencode/`, `.cursor/`, `.amazonq/`) sit outside both gates.
`harness bindings generate` emits them from `.claude/`, so any index written there is regenerated
away. `.claude/`, their source, is scanned instead.

## Finding Kinds

- `orphan` — a sibling `.md` file or subdirectory README exists but is unlinked.
- `ghost` — the index links a target that does not exist on disk.
- `missing` — a directory needs an index but has none.
- `unannotated` — the index links a target with no `- [<title>](<path>) — <description>
<when_to_use>` annotation (an em-dash or `--` followed by non-whitespace text).

## Remediation

`readme-index generate <dir>` behaves two ways. Given **no index** it scaffolds one in sorted order
— the `missing` remedy. Given one, it **edits, never rebuilds**: authored order, annotations,
headings, and prose survive byte-for-byte; only absent targets are spliced in. A target linked
anywhere, table cell included, counts as present, so `generate` is a no-op on a conforming tree.

`readme-index rewrite-paths --map <tsv>` repoints targets after a rename from `old<TAB>new` rows,
rewriting only what sits inside `](...)`. A malformed row errors rather than dropping a rename.

Fix `orphan`/`ghost`/`unannotated` by hand: add the link, drop the dangling one, or append
`— <description>` from the target's frontmatter (plus `when_to_use` if present). An annotation
repeating its surroundings adds nothing.

## Enforcement Points

Both gates run at pre-push (changed-path gated) and in CI's PR quality gate. Neither runs at
pre-commit — a whole-tree scan per commit adds no coverage over pre-push/CI.

## Updating Scope

Edit `args.paths`/`args.exclude`/`trigger` on the relevant `gates:` entry in `repo-config.yml`,
recording the rationale as a YAML comment.
