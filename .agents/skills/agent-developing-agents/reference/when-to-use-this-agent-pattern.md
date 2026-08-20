# Developing AI Agents — When to Use This Agent Pattern

Agents should include guidance on when to use them vs other agents, improving discoverability and preventing misuse.

## When to Use Pattern

Add "When to Use This Agent" section with two subsections:

```markdown
## When to Use This Agent

**Use when**:

- [Primary use case 1]
- [Primary use case 2]
- [Primary use case 3]
- [Specific scenario that fits]

**Do NOT use for**:

- [Anti-pattern 1] (use [other-agent] instead)
- [Anti-pattern 2] (use [alternative-tool/approach])
- [Edge case that doesn't fit]
- [Common misuse scenario]
```

## When to Include

**Highly Recommended for**:

- Agents with overlapping scopes (e.g., multiple checkers)
- Agents that users might confuse (e.g., maker vs editor)
- Agents with specific prerequisites (e.g., needs audit report)
- Specialized agents with narrow focus

**Examples by Agent Type**:

**Checker Agents**:

```markdown
## When to Use This Agent

**Use when**:

- Validating [domain] content before release
- Checking [domain] after updates
- Reviewing community contributions
- Auditing [domain] for compliance

**Do NOT use for**:

- Link checking (use [link-checker] instead)
- File naming/structure (use [rules-checker])
- Creating new content (use [maker-agent])
- Fixing issues (use [fixer-agent] after review)
```

**Fixer Agents**:

```markdown
## When to Use This Agent

**Use when**:

- After running [checker-agent] - You have an audit report
- Issues found and reviewed - You've reviewed checker's findings
- Automated fixing needed - You want validated issues fixed
- Safety is critical - You need re-validation before changes

**Do NOT use for**:

- Initial validation (use [checker-agent])
- Content creation (use [maker-agent])
- Manual fixes (use Edit tool directly)
- When no audit report exists
```

**Maker Agents**:

```markdown
## When to Use This Agent

**Use when**:

- Creating new [domain] content
- Need standardized structure/format
- Following [domain] conventions
- Building content from templates

**Do NOT use for**:

- Validating existing content (use [checker-agent])
- Fixing issues (use [fixer-agent])
- Bulk updates (use Edit tool for simple changes)
- Content outside [domain] scope
```

## Placement

Add "When to Use This Agent" section:

- After agent description or core responsibility
- Before detailed workflow/process sections
- Early in file for quick reference

## Benefits

✅ Improves agent discoverability
✅ Prevents misuse and confusion
✅ Clarifies agent boundaries
✅ Guides users to appropriate alternatives
✅ Reduces trial-and-error
