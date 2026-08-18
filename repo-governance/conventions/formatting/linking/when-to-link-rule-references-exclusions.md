---
title: "When to Link Rule References: Exclusions"
description: The cases where the two-tier link-then-inline-code formatting rule does not apply, and how the docs-checker agent validates the requirement.
when_to_use: Use when deciding whether a rule reference inside a code block, quote, file path, or naming discussion is exempt from the two-tier formatting rule.
category: explanation
subcategory: conventions
tags:
  - linking
  - markdown
  - conventions
  - github-compatibility
created: 2025-11-22
---

# When to Link Rule References: Exclusions

This two-tier formatting does NOT apply to:

- **Code blocks** - Already formatted as code
- **Quoted text** - Preserve original formatting
- **File path specifications** - Use literal paths
- **Meta-discussion about naming** - When discussing rule names as strings

**Example exclusions:**

````markdown
<!-- Code block - already formatted -->

```bash
# Apply linking-convention rules
validate_docs_links
```
````

<!-- Quoted text - preserve original -->

> The author wrote "see linking convention for details"

<!-- File path - literal path -->

The rule is defined in `repo-governance/conventions/formatting/linking.md`

<!-- Meta-discussion - discussing the name itself -->

We renamed "link-convention" to "linking-convention" for clarity

```

### Validation

The [docs-checker agent](../../../.claude/agents/docs/docs-checker.md) validates this two-tier formatting requirement:

- **First mention without link** → CRITICAL issue (breaks navigation)
- **Subsequent mention without inline code** → HIGH issue (convention violation)
- **All mentions improperly formatted** → CRITICAL issue (complete non-compliance)

```
