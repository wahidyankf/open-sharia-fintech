---
title: "Purpose and Scope"
description: What this workflow validates (repo-governance/, the primary binding directory agent and skill sources, docs/explanation/ partially) versus what it skips, and why.
when_to_use: Use when checking whether a specific directory or file family is in scope for this quality gate, or is delegated to a specialized agent family instead.
---

# Purpose and Scope

**Purpose**: Automatically validate repository consistency across principles, conventions,
development practices, agent and skill source definitions, and subdirectory README files, then
apply fixes iteratively until no finding at or above the selected mode threshold remains.

**IMPORTANT - Scope Clarification**:

This workflow validates **source definitions only**. Source includes governance docs, primary agent definitions, and primary skill packages — all of which live under version control and are authored by hand. It does NOT validate generated directories:

- PASS: **Validates**: `repo-governance/` (principles, conventions, development practices, workflows, vision)
- PASS: **Validates**: `.claude/agents/` (primary agent source definitions — agent-to-agent duplication, agent-Skill duplication, frontmatter compliance)
- PASS: **Validates**: `.claude/skills/` (primary agent-skill source — agent-skill-to-agent-skill consolidation opportunities and content quality). Non-vendored mirrors under `.agents/skills/` are rebuilt by `npm run generate:bindings`; registry-declared vendored plugin subtrees remain hand-maintained and are outside this workflow. `.claude/skills/` remains the authored source for generated mirrors.
- PASS: **Validates (partial)**: `docs/explanation/` through the AI checker for rules-governance and software-engineering alignment. The retained deterministic preflight covers only layer coherence and traceability; lifecycle-owned documentation predicates, including frontmatter checks, are consumed as exact external evidence rather than rerun here.
- FAIL: **Skips**: the rest of `docs/` (`docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/` non-software-engineering subtrees, `docs/metadata/`) — out of scope for this workflow today; validated by the specialized `docs/` agent family (`docs-checker`, `docs-tutorial-checker`, `docs-link-checker`, `docs-software-engineering-separation-checker`). Extending coverage to all of `docs/` is a backlog item — see [Backlog](./backlog.md).
  - **One carve-out to that skip**: Gherkin step-keyword cardinality (Step 7 sub-check 9) applies to
    ` ```gherkin ` fences **anywhere** in `docs/`, including the otherwise-skipped subtrees. The skip
    above is about document-level validation, not about that one cross-cutting fence rule.
- FAIL: **Skips**: generated platform bindings (for example `.opencode/agents/` and non-vendored
  mirrors under `.agents/skills/`) — rebuild them with `npm run generate:bindings`, then validate
  them with `rhino-cli harness bindings validate` / `npm run harness:bindings-validation`, not this
  workflow. Registry-declared vendored binding paths are skipped because they are external payloads,
  not because they are generated.

**Generated Output Validation**: Use CLI validation commands for validating generated content. This workflow ensures SOURCE is correct, then sync commands validate output generation.

**When to use**:

- After making changes to conventions, principles, or development practices
- Before major releases or deployments
- Periodically to ensure repository health
- After adding or modifying agents
