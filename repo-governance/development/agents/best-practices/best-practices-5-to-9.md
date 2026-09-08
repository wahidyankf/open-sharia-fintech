---
description: "Covers Practices 5-9: documenting tool usage in the agent body, testing with edge cases, frontmatter context, naming conventions, and documenting agent dependencies."
when_to_use: Use when finishing an agent definition and checking its tool-usage docs, test scenarios, naming, or dependency notes.
---

# Best Practices — Tool Usage Docs, Testing, Frontmatter Context, Naming, and Dependencies

## Practice 5: Document Tool Usage in Agent Body

**Principle**: Explain HOW the agent uses its tools in the agent body content.

**Good Example:**

```markdown
## Tool Usage

- **Read/Glob/Grep**: Scan documentation files for validation
- **WebFetch/WebSearch**: Verify external references and links
- **Write**: Generate audit reports in local-tmp/<agent-family>/
- **Bash**: Execute git commands for file operations
```

**Rationale:**

- Transparent behaviour
- Easier troubleshooting
- Clear security model

## Practice 6: Test Agents with Edge Cases

**Principle**: Test agents with both valid and invalid inputs before deployment.

**Good Example:**

```markdown
## Test Scenarios

1. Valid markdown file - should pass
2. File with broken links - should report errors
3. Empty file - should handle gracefully
4. Non-existent file - should report error
5. Very large file - should handle pagination
```

**Rationale:**

- Robust error handling
- Graceful degradation
- Production readiness

## Practice 7: Provide Context in Agent Frontmatter

**Principle**: Include enough context in frontmatter for the agent to work autonomously.

**Good Example:**

```yaml
---
context: |
  This agent validates tutorial documentation following Diátaxis framework.
  Tutorials are learning-oriented, hands-on, and beginner-friendly.
  Reports written to local-tmp/<agent-family>/ with UUID chains.
---
```

**Rationale:**

- Self-contained agents
- Reduced need for external documentation
- Consistent behaviour

## Practice 8: Follow Naming Conventions

**Principle**: Use descriptive kebab-case names following agent naming patterns.

**Good Example:**

```
docs-checker.md
apps-ayokoding-www-general-maker.md
plan-execution-checker.md
```

**Bad Example:**

```
checker.md
app1.md
my_agent.md
```

**Rationale:**

- Clear categorization
- Easy discovery
- Consistent organization

## Practice 9: Document Agent Dependencies

**Principle**: Clearly document what files, tools, or external services the agent depends on.

**Good Example:**

```yaml
---
dependencies:
  - local-tmp/<agent-family>/ directory must exist (agent creates it with mkdir -p)
  - WebSearch tool requires US region
  - Expects Diátaxis framework structure
---
```

**Rationale:**

- Clear requirements
- Easier troubleshooting
- Better onboarding
