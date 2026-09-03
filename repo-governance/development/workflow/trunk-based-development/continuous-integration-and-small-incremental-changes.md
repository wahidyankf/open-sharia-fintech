---
title: "Continuous Integration and Small, Incremental Changes"
description: What runs on every push, the pre-push checklist, and how to break work into small, independently reviewable commits.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use before pushing, to run the pre-push checklist, or when planning how to break a feature into small commits.
---

# Continuous Integration and Small, Incremental Changes

## Continuous Integration

**Every push triggers CI/CD** — on the PR under `*-to-pr` modes, and on `main` for direct pushes and after any merge:

1. **Automated tests** run on every push
2. **Build verification** ensures code compiles
3. **Linting and formatting** checks pass
4. **Deployment to staging** (optional, project-specific)

**CI failure is a high priority**:

- FAIL: **Never commit code that breaks CI**
- **If CI fails**, fix immediately (highest priority)
- **Broken `main` blocks everyone** - fix or revert

**Pre-push checklist**:

- [ ] All tests pass locally (`npm test`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] The resulting `main` state is safe to deploy to production immediately
- [ ] Incomplete behavior is complete-and-inert behind a temporary production-disabled feature flag
- [ ] Both flag paths pass and rollout, rollback, and removal are recorded
- [ ] Commit message follows [Conventional Commits](../commit-messages.md)

## Small, Thematic Changes

TBD favors the fewest build-valid, independently reviewable and revertible commits that express one
coherent purpose each. “Small” does not mean separating required completion artifacts, and numeric
LOC or file counts never create, erase, or force a PR boundary. Split delivery at natural cohesive
seams and keep everything required to build, verify, operate, roll back, and remain internally
consistent together.

PASS: **Good incremental changes**:

- Add a utility function with its required tests (commit 1)
- Use and extend it for one independently revertible feature (commit 2)

FAIL: **Bad large changes**:

- Rewrite entire authentication system in one commit
- Implement 5 features together in one PR
- Refactor + an independent feature in the same commit

**Benefits of cohesive changes**:

- **Faster reviews**: Reviewing 50 lines vs 5000 lines
- **Easier to revert**: If something breaks, revert is surgical
- **Clearer history**: Each commit has single, clear purpose
- **Reduced conflicts**: Less time diverged = fewer conflicts
- **Earlier feedback**: Team sees your work immediately

**How to break down work**:

1. **Identify a natural seam**: What independently useful purpose can safely deploy on its own?
2. **Complete that piece**: include required tests, docs, specs, references, generated artifacts,
   operations, and rollback support
3. **Repeat**: Build on top of previous work
4. **Use feature flags**: Keep incomplete behavior internally complete and inert behind a temporary
   production-disabled flag; test both paths and record rollout, rollback, and removal

**Example - "Add user login" broken down**:

```
Commit 1: feat(auth): add User model with email field
Commit 2: feat(auth): add password hashing utility
Commit 3: feat(auth): add login endpoint (feature flag OFF)
Commit 4: feat(auth): add login UI component (feature flag OFF)
Commit 5: feat(auth): connect UI to endpoint (feature flag OFF)
Commit 6: feat(auth): enable login feature flag in staging
Commit 7: feat(auth): enable login feature flag in production
Commit 8: refactor(auth): remove old login code and feature flag
```

Each commit includes the tests and documentation required for its purpose and leaves `main` safe to
deploy to production. Each PR groups commits at one natural seam and integrates promptly once ready.
