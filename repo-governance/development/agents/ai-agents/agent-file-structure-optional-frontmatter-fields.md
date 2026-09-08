---
description: "Defines optional frontmatter fields an agent definition may include beyond the required set."
when_to_use: Use when deciding whether to add an optional frontmatter field to an agent.
---

# Agent File Structure — Optional Frontmatter Fields

In addition to the six required fields, agents may include optional metadata fields for tracking:

1. **`created`** (optional)
   - Date when the agent was first created
   - Format: `YYYY-MM-DD` (ISO 8601 date only)
   - Example: `created: 2025-11-23`
   - Helps track agent age and history

**Note**: The `updated:` field is NOT used in agent frontmatter. Per the [No Manual Date Metadata Convention](../../../conventions/structure/no-date-metadata.md), non-website markdown files must not carry `updated:` fields — git history is the authoritative change record.

**Best Practices:**

- Use `created` to record when the agent was first added
- Do NOT add `updated:` — use `git log --follow -- <file>` to find when an agent was last changed
- Use consistent date format (YYYY-MM-DD) matching the project's [Timestamp Format Convention](../../../conventions/formatting/timestamp.md) (date-only format)
- Place these fields after the six required fields in frontmatter

**Example with optional fields:**

```yaml
---
name: agent-name
description: Expert in X specializing in Y. Use when Z.
tools: Read, Glob, Grep
model:
color: blue
skills: []
created: 2025-11-23
---
```
