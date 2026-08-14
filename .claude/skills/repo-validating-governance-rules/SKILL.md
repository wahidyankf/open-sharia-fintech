---
name: repo-validating-governance-rules
description: Complete validation methodology for repository-wide governance consistency — file naming/linking/emoji, agent-Skill and Skill-to-Skill duplication/consolidation, governance word budgets, rules-governance contradictions/traceability/licensing/dependency-bump-policy, and software-engineering documentation quality. Used by repo-rules-checker.
---

# Validating Repository Governance Rules

Methodology for `repo-rules-checker`, which validates repository-wide consistency across all
governance layers, agent/Skill duplication, and software-engineering documentation.

## Reference Modules

1. [reference/01-core-and-skills-validation.md](reference/01-core-and-skills-validation.md) —
   Core Repository Validation (naming, linking, emoji, No-Last-Updated), Agent-to-Agent
   Duplication, Agent-Skill Duplication, Skill-to-Skill Consolidation, Skills Coverage Gaps.
2. [reference/02-word-budget-and-rules-governance.md](reference/02-word-budget-and-rules-governance.md) —
   governance word-budget delegation, contradictions/inaccuracies/inconsistencies, traceability,
   layer coherence, licensing compliance, dependency-bump policy compliance, Gherkin
   step-keyword cardinality.
3. [reference/03-software-docs-validation.md](reference/03-software-docs-validation.md) —
   the eight `docs/explanation/software-engineering/` sub-checks (principle alignment,
   cross-references, naming, structure, templates, diagrams, README index, version docs).
4. [reference/04-preflight-and-report-structure.md](reference/04-preflight-and-report-structure.md) —
   consuming the deterministic `rhino-cli repo-governance audit` preflight JSON, the execution
   step sequence, and the final two-section report structure.

## Core Principles

**Deterministic-first**: every step that has a `rhino-cli`/`nx` deterministic gate defers to it —
never re-derive what a mechanical validator already checks; only judge the AI-only, qualitative
portion. **Progressive writing**: every finding is written immediately, never buffered — Step 8
(~265 files) is the step most likely to be interrupted by compaction. **Conservative
consolidation**: when uncertain whether Skills should merge, recommend KEEP SEPARATE.

## Related

**Conventions**: all conventions in `repo-governance/conventions/`, all practices in
`repo-governance/development/`, [AI Agents Convention](../../../repo-governance/development/agents/ai-agents.md).

**Agents**: `repo-rules-checker` (implements this methodology), `repo-rules-fixer`,
`repo-rules-maker`.
