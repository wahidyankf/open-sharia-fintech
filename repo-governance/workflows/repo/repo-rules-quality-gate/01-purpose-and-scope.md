---
title: "Purpose and Scope"
description: What this workflow validates (repo-governance/, the primary binding directory agent and skill sources, docs/explanation/ partially) versus what it skips, and why.
when_to_use: Use when checking whether a specific directory or file family is in scope for this quality gate, or is delegated to a specialized agent family instead.
---

# Purpose and Scope

**Purpose**: Automatically validate repository consistency across principles, conventions, development practices, agent and skill source definitions, and subdirectory README files, then apply fixes iteratively until all issues are resolved.

**IMPORTANT - Scope Clarification**:

This workflow validates **source definitions only**. Source includes governance docs, primary agent definitions, and primary skill packages — all of which live under version control and are authored by hand. It does NOT validate generated directories:

- PASS: **Validates**: `repo-governance/` (principles, conventions, development practices, workflows, vision)
- PASS: **Validates**: `.claude/agents/` (primary agent source definitions — agent-to-agent duplication, agent-Skill duplication, frontmatter compliance)
- PASS: **Validates**: `.claude/skills/` (primary agent-skill source — agent-skill-to-agent-skill consolidation opportunities, agent-skill content quality). Agent skills are NOT mirrored to secondary bindings — primary binding skill packages are read natively by all supporting coding-agent platforms, so `.claude/skills/` IS the source of truth and IS in scope.
- PASS: **Validates (partial)**: `docs/explanation/` (Diátaxis tree — preflight frontmatter audit covers tutorial / how-to / reference / explanation per the Diátaxis schema; software-engineering subtree validated by Step 8 in the AI checker for principle alignment, README index accuracy, and version documentation) and `docs/explanation/README.md` (Diátaxis explanation index — Step 1 Rules Governance scope) and `docs/explanation/software-engineering/` (~265 files / 345k lines — Step 8 dedicated validation: governance-principle alignment, cross-reference completeness, file naming, document structure, template completeness, diagram accessibility, README index accuracy, version documentation).
- FAIL: **Skips**: the rest of `docs/` (`docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/` non-software-engineering subtrees, `docs/metadata/`) — out of scope for this workflow today; validated by the specialized `docs/` agent family (`docs-checker`, `docs-tutorial-checker`, `docs-link-checker`, `docs-software-engineering-separation-checker`). Extending coverage to all of `docs/` is a backlog item — see [Backlog](./19-backlog.md).
  - **One carve-out to that skip**: Gherkin step-keyword cardinality (Step 7 sub-check 9) applies to
    ` ```gherkin ` fences **anywhere** in `docs/`, including the otherwise-skipped subtrees. The skip
    above is about document-level validation, not about that one cross-cutting fence rule.
- FAIL: **Skips**: secondary platform binding agent directories (e.g., `.opencode/agents/`) — auto-generated from `.claude/agents/` via `npm run generate:bindings`. Validate via the sync script + `cross-vendor:parity-validation` Nx target, not this workflow.

**Generated Output Validation**: Use CLI validation commands for validating generated content. This workflow ensures SOURCE is correct, then sync commands validate output generation.

**When to use**:

- After making changes to conventions, principles, or development practices
- Before major releases or deployments
- Periodically to ensure repository health
- After adding or modifying agents
