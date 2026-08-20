---
title: "Glossary"
description: Shared vocabulary for the repository — the terms whose scope is genuinely disputed, defined once so contributors and agents mean the same thing.
when_to_use: Use when a term's scope is in question, when a rule's reach is being argued, or when writing governance prose that leans on one of these terms.
category: explanation
subcategory: governance
tags:
  - governance
  - glossary
  - conventions
  - agents
created: 2026-08-16
---

# Glossary

This glossary defines only genuinely ambiguous terms — the ones where two readers reasonably
disagree about what a rule covers. Terms their own convention already defines are not repeated;
each entry links to the authoritative document instead.

The recurring source of disagreement: **normativity does not follow the directory tree**. Where a
term names a set that crosses directory boundaries, this glossary says so explicitly.

## Repo Rules

**Repo rules** means every surface that binds how work happens in this repository, regardless of
where it sits. It is a semantic set, not a directory: `repo-governance/`, the canonical instruction
file and its binding shims, agent definitions and agent skill files, the generated binding mirrors,
the machine-readable declarations in `repo-config.yml`, the enforcement machinery that makes those
declarations bite, and the language style guides under `docs/explanation/software-engineering/`.

The set is deliberately wider than `repo-governance/`. A rule stated in a gate declaration or a
style guide binds exactly as much as one stated in a convention document; only its encoding differs.

## Children

- [Repo Rules — Scope Boundaries](./glossary/repo-rules-scope.md) — the in-scope and out-of-scope
  table, including why the language style guides are in scope despite living outside
  `repo-governance/`.
- [Content Trees](./glossary/content-trees.md) — what belongs in `docs/`, `repo-governance/`,
  `plans/`, and `specs/`, and the sweepable temporary directories.
- [Plan Vocabulary](./glossary/plan-vocabulary.md) — plan, phase, delivery unit, delivery
  boundary, delivery mode, and worktree.
- [Governance Surfaces](./glossary/governance-surfaces.md) — surface, instruction file, binding,
  mirror, harness, and what "autoloaded" actually means.
- [The `class: vendored` Exception Has Two Subclasses](./glossary/vendored-exception-subclasses.md) — delimited-region
  vs. wholly external, and why confusing one for the other misfires in opposite directions.
- [Agent Vocabulary](./glossary/agent-vocabulary.md) — agent, agent skill, gate, quality gate,
  workflow, and the maker/checker/fixer roles.
- [Principles and Related Conventions](./glossary/principles-and-related-conventions.md) — Which
  principles the glossary implements and which conventions authoritatively define the terms it
  names. Use when tracing a glossary entry upward to the principle it serves or downward to the
  convention that governs it.
