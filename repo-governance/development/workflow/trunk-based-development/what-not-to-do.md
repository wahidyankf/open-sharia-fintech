---
description: A ten-row anti-pattern-versus-TBD-approach table covering branch lifespan, commit granularity, and CI-gating mistakes.
when_to_use: Use as a quick reference to spot a TBD anti-pattern in a proposed workflow.
---

# What NOT to Do

| FAIL: Anti-Pattern                   | PASS: TBD Approach                                                                                                     |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Long-lived feature branches          | Commit to `main` with feature flags                                                                                    |
| Branches per developer               | All developers commit to `main`                                                                                        |
| Delaying integration for weeks       | Integrate multiple times per day                                                                                       |
| Large, infrequent commits            | Small, frequent commits (see [Commit Granularity](../commit-messages/commit-granularity-and-when-to-split-commits.md)) |
| Keeping branches "just in case"      | Delete branches immediately after merge                                                                                |
| Using branches to hide WIP           | Integrate complete-and-inert work behind a tested temporary production-disabled flag                                   |
| Merging without CI passing           | CI must be green before merge                                                                                          |
| Long-lived branches surviving days   | Branches (if used) stay short-lived -- merge within 1-2 days                                                           |
| Waiting for "perfect" code to commit | Commit working code, iterate in subsequent commits                                                                     |
| Feature branches lasting weeks       | Branches (if used) last < 2 days                                                                                       |
