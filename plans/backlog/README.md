# Backlog Plans

Planned projects for future implementation.

## Planned Projects

- [2026-07-18\_\_rhino-cli-git-root-test-fixture-race](./2026-07-18__rhino-cli-git-root-test-fixture-race/README.md) —
  a rhino-cli git-root test fixture races under parallel `nx affected`, corrupting the real
  repository's git state (stray commits, stray linked worktrees, mis-attributed authorship).
- [2026-07-18\_\_e2e-coverage-rule-feature-skip-fixme-gap](./2026-07-18__e2e-coverage-rule-feature-skip-fixme-gap/README.md) —
  the e2e-coverage gap detector's `@skip`/`@fixme` special-tag detection is scoped to
  `Scenario Outline` level only; `Rule:`/`Feature:`-level tags produce the same undetected shape one
  AST level up.

## Instructions

**Quick Idea Capture**: For 1-3 liner ideas not ready for formal planning, use `../ideas.md`.

When creating a new plan:

1. Create folder: `YYYY-MM-DD__[project-identifier]/`
2. Add standard files: README.md, brd.md, prd.md, tech-docs.md, delivery.md
3. Add the plan to this list
