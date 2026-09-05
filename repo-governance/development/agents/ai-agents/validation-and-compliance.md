---
title: "Validation and Compliance"
description: "Explains how rules-checker validates agent compliance and how to manually verify an agent."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when running or interpreting an agent-compliance validation pass.
---

# Validation and Compliance

## Repo-Rule-Checker Integration

The `rules-checker` agent validates all agents against this convention.

**Checks performed:**

1. PASS: Frontmatter has all required fields
2. PASS: Agent `name` matches filename
3. PASS: Agent `description` provides clear usage guidance
4. PASS: Agent `tools` field lists tools explicitly
5. PASS: Agent `model` field is present and valid
6. PASS: Document structure follows standard pattern
7. PASS: Reference documentation section exists
8. PASS: References to AGENTS.md and this convention present
9. PASS: Links use GitHub-compatible format

## Manual Verification

Before committing a new agent:

1. **Read this entire convention** - Understand all requirements
2. **Use the agent creation checklist** - Verify all items
3. **Test the agent** - Invoke it and verify behaviour
4. **Review existing agents** - Ensure consistency
5. **Run rules-checker** - Validate compliance
