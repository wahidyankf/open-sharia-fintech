---
description: "Gives the step-by-step procedure for assigning a color to a newly created agent."
when_to_use: Use when creating a new agent and choosing its color field value.
---

# Platform Binding Examples — Assigning Colors to New Agents

When creating a new agent, assign a color based on its **primary capability**:

**Decision Tree:**

```
Start: What is the agent's primary capability?
    │
    ├─ Creates new files/content from scratch
    │   └─> color: blue (Maker)
    │       - Must have `Write` tool
    │       - Examples: docs-maker, plan-maker
    │
    ├─ Validates/checks and generates reports
    │   └─> color: green (Checker)
    │       - Has `Write`, `Bash` (no Edit)
    │       - Write needed for audit reports in local-tmp/<agent-family>/
    │       - Bash needed for UTC+7 timestamps
    │       - Examples: rules-checker, plan-checker, docs-checker
    │       - EXCEPTION: Link checkers also have Edit tool for cache management (see "Link Checker Agents Note" below)
    │
    ├─ Modifies/updates existing content only
    │   └─> color: yellow (Fixer)
    │       - Has `Edit` but NOT `Write`
    │       - Examples: docs-file-manager, readme-fixer, repo-workflow-fixer
    │
    └─ Executes plans/orchestrates tasks
        └─> color: purple (Implementor)
            - Has Write, Edit, AND Bash
            - Examples: swe-*-dev agents; plan execution itself is orchestrated by the calling context via the plan-execution workflow (no dedicated subagent)
```

**Edge Cases:**

- **Agent has both Write and Edit**: Choose based on primary purpose
  - If mainly creates new content → `blue` (Maker)
  - If mainly executes plans/tasks → `purple` (Implementor)
- **Link-checkers with Write, Edit, Bash**: Use `green` (Checker)
  - Write tool needed for audit reports in `local-tmp/<agent-family>/`
  - Edit tool needed for cache file management (external-links-status.yaml updates)
  - Bash tool needed for UTC+7 timestamps
  - Examples: docs-link-checker, apps-ayokoding-www-link-checker
- **Deployers with Bash only**: Use `purple` (Implementor)
  - Execute deployment orchestration (purple's "executes plans/orchestrates tasks")
  - Don't create or edit files, only run git/deployment commands
  - Edge case: purple without Write/Edit tools (Bash-only orchestration)
  - Examples: apps-ayokoding-www-deployer, apps-ose-www-deployer, apps-organiclever-app-web-deployer
- **Fixers with Write tool**: Investigate actual usage
  - Yellow (Fixers) should have Edit but NOT Write
  - If Write is needed for creating new convention files → keep yellow, document exception
  - If Write can be removed → remove Write to match yellow categorization
  - Example: readme-fixer, repo-workflow-fixer (fixer agents that generate audit reports, keep Write for report writing)
- **Agent doesn't fit any category**: Consider if it should be split or if a new category is needed
- **Unsure**: Default to the most restrictive category based on tools, or omit the color field

**Accessibility Note**: All assigned colors (blue, green, yellow, purple) are verified color-blind friendly and meet WCAG accessibility standards per the [Color Accessibility Convention](../../../conventions/formatting/color-accessibility.md). Agents should still be identified primarily by name and role suffix, not color alone, to ensure accessibility for all users. See the Color Accessibility Convention for complete details on palette verification, testing methodology, and WCAG compliance.
