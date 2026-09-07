---
description: Recap of all twelve best practices, plus the principles and conventions they implement.
when_to_use: Use as a quick recap of all twelve practices, or when tracing them back to the principles and conventions they implement.
---

# Summary and Principles/Conventions Implemented

## Summary

Following these best practices ensures:

1. Integrate continuously via short-lived branches
2. Compose the fewest build-valid, reviewable, and revertible commits
3. Use Conventional Commits
4. Integrate complete-and-inert behaviour behind temporary production-disabled flags, with both
   paths tested and rollout, rollback, and removal recorded
5. Implement in three stages (work → right → fast)
6. Pin dependencies for reproducibility
7. Keep CI green at all times
8. Use environment-specific configuration
9. Split independently reviewable purposes, not file domains
10. Test before committing
11. Pull with rebase before pushing (linear history for TBD)
12. Default to `worktree-to-pr`; select a direct-push mode deliberately

Workflows built following these practices are efficient, predictable, and high-quality.

## Principles Implemented/Respected

- **Simplicity Over Complexity**: Single branch, fewest qualifying commits, clear workflow
- **Automation Over Manual**: CI enforcement, automated testing
- **Reproducibility First**: Pinned dependencies, environment configuration
- **Explicit Over Implicit**: Conventional Commits, clear commit messages

## Conventions Implemented/Respected

- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Active voice, clear documentation of workflow practices
- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Workflow documents follow standardized kebab-case naming
- **[Linking Convention](../../../conventions/formatting/linking.md)**: GitHub-compatible links to related workflow documentation
