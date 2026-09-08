---
description: Standard validation methods and patterns for repository consistency checking
when_to_use: "Use when writing or debugging a repository-wide validation check."
---

# Repository Validation Methodology Convention

This convention defines the standard patterns for validating repository-wide consistency -- frontmatter extraction, common checks, and the pitfalls a validation script must avoid.

## Documents

- [Principles and Conventions Implemented/Respected](./repository-validation/principles-and-conventions-implemented-respected.md) — Principles/conventions implemented. Use to trace this convention's rationale.
- [Overview](./repository-validation/overview.md) — Overview of the repository validation methodology. Use when orienting to how repository validation works.
- [The Frontmatter Extraction Pattern (CRITICAL)](./repository-validation/the-frontmatter-extraction-pattern-critical.md) — The critical pattern for extracting frontmatter safely in validation scripts. Use when writing a script that extracts frontmatter from a markdown file.
- [Standard Validation Checks (1-3)](./repository-validation/standard-validation-checks-1-3.md) — Checks 1-3: frontmatter comments, missing fields, wrong field values. Use when implementing or debugging one of the first three standard checks.
- [Standard Validation Checks (4-5)](./repository-validation/standard-validation-checks-4-5.md) — Checks 4-5: broken link detection, file naming convention. Use when implementing or debugging the link or naming checks.
- [Best Practices](./repository-validation/best-practices.md) — Best practices for writing repository validation checks. Use when writing a new repository validation check.
- [Common Pitfalls](./repository-validation/common-pitfalls.md) — Common pitfalls when writing validation scripts. Use when debugging a validation script that behaves unexpectedly.
- [Markdown Quality Gates](./repository-validation/markdown-quality-gates.md) — The markdown-specific quality gates and their commands. Use when locating a markdown quality gate's command or exclusions.

## Maintenance Notes

When adding new validation checks:

1. **Document the pattern** in this convention
2. **Provide working examples** with correct and incorrect usage
3. **Explain the pitfalls** and how to avoid them
4. **Test edge cases** before deploying to agents
5. **Update related agents** to use the standardized pattern

When existing checks fail:

1. **Verify the pattern** matches this convention
2. **Check for edge cases** not covered by standard pattern
3. **Update this convention** if pattern needs refinement
4. **Propagate changes** to all agents using the pattern

This convention is the single source of truth for validation logic. All agents should reference and implement these patterns consistently.

## Related Conventions

- [AI Agents Convention](../agents/ai-agents.md) - Agents that use these validation methods
- [File Naming Convention](../../conventions/structure/file-naming.md) - What we validate (naming patterns)
- [Linking Convention](../../conventions/formatting/linking.md) - What we validate (link formats)
- [Temporary Files Convention](../infra/temporary-files.md) - Where validation reports are stored
- [Diagram and Schema Convention](../../conventions/formatting/diagrams.md) - Mermaid enforcement details
- [Content Quality Principles](../../conventions/writing/quality.md) - Heading hierarchy enforcement details
