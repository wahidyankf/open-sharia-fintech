---
description: "Defines required and recommended documentation elements and writing style for agent definition files."
when_to_use: Use when writing or reviewing the prose quality of an agent definition file.
---

# Agent Documentation Standards

## Required Elements

Every agent must include:

1. PASS: **Clear purpose statement** - What does this agent do?
2. PASS: **Core expertise/responsibility** - What is it an expert in?
3. PASS: **Usage guidelines** - When should you use this agent?
4. PASS: **Reference documentation** - Links to conventions and related docs

## Recommended Elements

Depending on complexity, consider adding:

- **Examples** - Show the agent in action
- **Anti-patterns** - What NOT to do
- **Checklists** - Step-by-step verification
- **Decision trees** - Help users make decisions
- **Troubleshooting** - Common issues and solutions

## Writing Style

Follow these guidelines when writing agent documentation:

1. **Use imperative, direct language**
   - PASS: "Use this agent when creating documentation"
   - FAIL: "This agent could potentially be used for documentation tasks"

2. **Be action-oriented**
   - PASS: "Validates consistency between files"
   - FAIL: "Performs validation activities"

3. **Provide concrete examples**
   - Include code snippets, file examples, command outputs
   - Show both good () and bad () examples

4. **Use checklists where applicable**
   - Break complex tasks into verifiable steps
   - Use `- [ ]` format for actionable items

5. **Be specific, not vague**
   - PASS: "Checks file naming against ex-co\_\_file-naming-convention.md"
   - FAIL: "Validates files"

6. **Follow indentation convention**
   - Agent files are in the platform binding directories (outside `docs/`), so use standard markdown (spaces for indentation)
   - When agents create/edit files in `docs/`, they must use TAB indentation for nested bullets
   - YAML frontmatter always uses spaces (2 spaces per level) regardless of file location
