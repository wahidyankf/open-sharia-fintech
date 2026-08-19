---
name: repo-understanding-shared-vocabulary
description: Shared repository vocabulary — what "repo rules", the four content trees, delivery units, and governance surfaces actually cover. Auto-loads when a task involves repository rules, governance scope, plans, delivery units, agent or skill boundaries, or any judgement about whether a rule reaches a given file.
when_to_use: Use before deciding what a rule covers, which tree a file belongs in, or whether two pieces of work are one delivery unit or two.
---

# Shared Repository Vocabulary

Delegated agents do not inherit the canonical instruction file, so this Skill is how the shared
vocabulary reaches them. It carries operative meanings only; where it and the glossary differ, the
glossary wins.

Most scope disputes are vocabulary disputes in disguise: two readers who disagree about whether a
rule applies usually agree on the rule and disagree on one word in it.

## The terms

- **Repo rules** — every surface that binds how work happens, wherever it sits. Not a synonym for
  one directory: governance prose, the root instruction surfaces, agent and skill definitions,
  generated mirrors, the config's machine-readable declarations, the hooks and pipeline jobs
  enforcing them, and the language style guides. A sweep scoped to one tree skips most of it. See
  [Repo Rules — Scope Boundaries](../../../repo-governance/glossary/repo-rules-scope.md).
- **Content trees** — four trees differing by who is bound and for how long, not by subject: one
  describes the product, one binds contributors, one holds work that expires, one holds acceptance
  criteria. See
  [Content Trees](../../../repo-governance/glossary/content-trees.md).
- **Delivery unit** — the unit a branch and a PR map to: a contiguous run of phases that ships on
  its own. A phase is smaller, and mapping a PR to a phase is the common error. See
  [Plan Vocabulary](../../../repo-governance/glossary/plan-vocabulary.md).
- **Surface and binding** — a surface is the file class a gate measures; a binding is the
  harness-specific configuration, one hand-authored and the rest generated. "Autoloaded" is
  narrow — a link inside an autoloaded file is not itself autoloaded. See
  [Governance Surfaces](../../../repo-governance/glossary/governance-surfaces.md).
- **Agent, skill, gate, workflow** — distinguished by what holds the knowledge and who decides when
  it runs. See [Agent Vocabulary](../../../repo-governance/glossary/agent-vocabulary.md).

## Related Skills

- `repo-understanding-repository-architecture` — orthogonal: that Skill covers how the six
  governance layers relate, this one what individual terms cover. Consult both when placing a new
  document.

---

**Note**: [the governance glossary](../../../repo-governance/glossary.md) is the source of truth;
this Skill is its delivery vehicle for delegated agents.
