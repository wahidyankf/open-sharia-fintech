# E2E Scenario Coverage Gap Detector

## Summary

`playwright-bdd`'s `missingSteps: skip-scenario` setting silently converts any Gherkin scenario
lacking an e2e step definition into `test.fixme`, with no build or CI failure. Nothing in the
pipeline currently compares "scenarios declared in a `.feature` file" against "scenarios actually
bound at each test level" — the gap is only caught by a human or agent manually running `bddgen`
and counting. Add a mechanical validator that catches this automatically.

## Origin

Surfaced during `plans/done/2026-07-15__ayokoding-resizable-docs-sidebar`'s PR-Review
Maker→Fixer cycle 3 (`ayokoding-www-fe-e2e`): only 3 of `resizable-panel.feature`'s 10 scenarios
had e2e step defs bound; the other 7 silently became `test.fixme`. This is the **second**
occurrence of the same root cause in the same PR — cycle 1 had already flagged an equivalent gap
as a MEDIUM finding and "resolved" it via an in-comment justification for keeping
`missingSteps: skip-scenario` project-wide rather than switching to `fail-on-gen`. The documented
justification did not prevent recurrence; a fresh gap was reintroduced on a different feature file
within the same PR. See the Knowledge Capture entry in that plan's `learnings.md` for full context.

## Status

Backlog — not yet scoped into requirements/tech-docs/delivery detail. Filed per the
[Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)'s
code-routing downstream rule (code-homed learnings are always filed as backlog, never landed
inline in the originating plan's PR).

## Related

- [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
- [BDD Spec-to-Test Mapping](../../../repo-governance/development/infra/bdd-spec-test-mapping.md)
