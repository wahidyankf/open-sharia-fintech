# Database Internals Course Ruff Configuration

## Context

`database-internals-and-storage-engines` contains runnable Python examples, drills, and a capstone.
It lacks the course-scoped Ruff configuration used by other annotated-concept courses. A formatter
therefore falls back to its default line length and can wrap explanatory trailing annotations into
unannotated physical lines.

## Scope

**In scope**: add one course-root `ruff.toml` and verify that Ruff accepts and preserves the existing
Python corpus. **Out of scope**: changing instructional prose, Python logic, test expectations,
manifests, routes, shared lint configuration, or unrelated course formatting.

**Affected surface**: `apps/ayokoding-www` course content only. The plan changes lint configuration,
not user-facing runtime behavior.

## Approach Summary

Establish a formatter baseline, derive the narrowest viable course-local line length, add the scoped
configuration, and prove Ruff format checks the existing corpus without changing files. This remains
separate from Learning Path 04 because it is a code-adjacent configuration repair.

## Delivery

- **Delivery mode**: `worktree-to-pr`.
- **Worktree**: `worktrees/ayokoding-database-internals-ruff-config/`.
- **Dependencies**: none.
- **Blocking relationship**: independent of Learning Path 04 delivery after this plan was filed.

Read the supporting documents before execution:

- [Business requirements](./brd.md)
- [Product requirements](./prd.md)
- [Technical approach](./tech-docs.md)
- [Delivery checklist](./delivery.md)
