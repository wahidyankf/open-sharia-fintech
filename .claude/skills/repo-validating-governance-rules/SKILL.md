---
name: repo-validating-governance-rules
description: Complete validation methodology for repository-wide governance consistency — file naming/linking/emoji, agent-Skill and Skill-to-Skill duplication/consolidation, governance word budgets, rules-governance contradictions/traceability/licensing/dependency-bump-policy, and software-engineering documentation quality. Used by repo-rules-checker.
---

# Validating Repository Governance Rules

Methodology for `repo-rules-checker`, which validates repository-wide consistency across all
governance layers, agent/Skill duplication, and software-engineering documentation.

## Reference Modules

1. [01-core-validation-and-agent-duplication.md](reference/core-validation-and-agent-duplication.md)
   and [02-skills-duplication-and-report-formats.md](reference/skills-duplication-and-report-formats.md) —
   Core Repository Validation (naming, linking, emoji, No-Last-Updated), Agent-to-Agent
   Duplication, Agent-Skill Duplication, Skill-to-Skill Consolidation, Skills Coverage Gaps, and
   the finding report formats.
2. [03-word-budget-and-rules-governance-core.md](reference/word-budget-and-rules-governance-core.md)
   and [04-rules-governance-licensing-and-dependency-policy.md](reference/rules-governance-licensing-and-dependency-policy.md) —
   governance word-budget delegation, contradictions/inaccuracies/inconsistencies, traceability,
   layer coherence, licensing compliance, dependency-bump policy compliance, Gherkin
   step-keyword cardinality.
3. [05-software-docs-validation-8-1-to-8-4.md](reference/software-docs-validation-8-1-to-8-4.md)
   and [06-software-docs-validation-8-5-to-8-8.md](reference/software-docs-validation-8-5-to-8-8.md) —
   the eight `docs/explanation/software-engineering/` sub-checks (principle alignment,
   cross-references, naming, structure, templates, diagrams, README index, version docs).
4. [07-preflight-consumption.md](reference/preflight-consumption.md) and
   [08-execution-sequence-and-report-structure.md](reference/execution-sequence-and-report-structure.md) —
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
