# Technical Documentation: E2E Scenario Coverage Gap Detector

## Status

Not yet designed — this plan is filed at backlog depth (README + brd + prd) per the
[Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)'s
code-routing downstream rule. Full technical design (validator implementation approach, baseline
storage format, CI wiring) is deferred to this plan's own planning pass when it is promoted from
`backlog/` to `in-progress/` via the standard
[plan-execution workflow](../../../repo-governance/workflows/plan/plan-execution.md), at which
point `plan-maker` should grill the assignee on the open questions listed in `prd.md`.

## Relevant Prior Art

- `apps/ayokoding-www-fe-e2e/playwright.config.ts` — the `missingSteps: skip-scenario` config and
  its existing in-comment justification (the artifact this validator supersedes/backstops).
- `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/**` and
  `specs/libs/web-ui/behavior/gherkin/**` — the Gherkin feature files this validator would scan.
- `plans/ideas.md` — the current informal tracking location for the ~104-scenario pre-existing
  gap; candidate source for the initial baseline.
- `repo-governance/development/infra/bdd-spec-test-mapping.md` — the existing convention governing
  how Gherkin specs map to test levels; this validator's output should be consistent with that
  mapping's terminology.
- `.claude/agents/ci-checker.md` and `.claude/agents/pr-review-maker.md` — candidate consumers of
  this validator's signal.
