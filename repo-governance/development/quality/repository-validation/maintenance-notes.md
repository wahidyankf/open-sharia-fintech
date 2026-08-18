---
title: "Maintenance Notes"
description: "Notes for maintaining the validation scripts over time."
category: explanation
subcategory: development
tags:
  - validation
  - consistency
  - bash
  - awk
  - frontmatter
  - automation
created: 2025-12-14
when_to_use: "Use when updating or extending a repository validation script."
---

# Maintenance Notes

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
