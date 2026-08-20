---
name: agent-developing-agents
description: AI agent development standards including frontmatter structure, naming conventions, tool access patterns, model selection, and reference documentation structure
---

# Developing AI Agents

Comprehensive guidance for creating AI agents following repository conventions.

## Core Requirements

- Frontmatter: name, description, tools, model, color, skills
- Name must match filename exactly
- Non-empty skills field required

## File Operations in .claude/ and .opencode/ Directories

Use the normal `Write` / `Edit` tools to create and modify files under `.claude/` and `.opencode/`. Both paths are pre-authorized in `.claude/settings.json`, so no approval prompts fire. `Bash` heredoc and `sed` remain appropriate for bulk mechanical substitutions across many files.

This applies to `.claude/agents/*.md`, `.claude/skills/*/SKILL.md` and `reference/*.md`, and their generated mirrors (`.opencode/agents/*.md`, `.codex/agents/*.toml`, `.agents/skills/`). After editing `.claude/` sources, run `npm run generate:bindings` so every mirror stays aligned — the regenerated mirrors are part of your change and MUST land in the **same commit** as the `.claude/` source. Verify with `npm run harness:bindings-validation`, which covers every harness including `.codex/`; `npm run validate:sync` does not. Every generated mirror MUST NOT be hand-edited — except a path an entry's `ownership:` list declares `vendored`, which covers two structurally different subclasses; see [the two vendored subclasses](../../../repo-governance/glossary/vendored-exception-subclasses.md) for which one applies before hand-editing. See also [File-Touch Discipline](../../../repo-governance/development/practice/file-touch-discipline.md).

## References

[AI Agents Convention](../../../repo-governance/development/agents/ai-agents.md)

## Tool Usage Documentation

Agents with 4+ tools, unusual tool combinations, or non-obvious tool choices should document a "Tools Usage" section listing each tool and its purpose, placed after the core responsibility and before detailed workflow sections. See [Tool Usage Documentation](./reference/tool-usage-documentation.md) for the pattern and worked examples by agent family (checker/fixer/maker).

## When to Use This Agent

Agents with overlapping scope or that users might confuse should include a "When to Use This Agent" section with "Use when" / "Do NOT use for" subsections, placed early in the file. See [When to Use This Agent Pattern](./reference/when-to-use-this-agent-pattern.md) for the pattern, worked examples by agent family, and placement guidance.

## Documenting Agent References

All agents SHOULD include a standardized "Reference Documentation" section near the end (before appendices), with four subsections: Project Guidance, Related Agents, Related Conventions, Skills. See [Documenting Agent References](./reference/documenting-agent-references.md) for the section template and subsection-by-subsection guidance, and [Reference Documentation Placement and Examples](./reference/documenting-agent-references-examples.md) for file placement and worked examples across the docs/readme/plan agent families.

## Selecting AI Models for Agents

Choose `sonnet` for tasks requiring judgment, ambiguity resolution, or multi-step orchestration; choose `haiku` for deterministic, pattern-matching, or high-volume tasks. Document the choice with a "Model Selection Justification" near the top of the agent file. See [Decision Framework](./reference/selecting-ai-models-decision-framework.md) for model characteristics and the full sonnet-vs-haiku criteria, [Matrix and Examples](./reference/selecting-ai-models-examples.md) for the selection matrix and agent-specific worked examples, [Documenting Model Selection and Cost Trade-offs](./reference/selecting-ai-models-documenting-and-costs.md) for the justification pattern and cost/performance trade-offs, and [Model Selection Checklist and Common Mistakes](./reference/selecting-ai-models-checklist-and-mistakes.md) for the pre-selection checklist and anti-patterns.
