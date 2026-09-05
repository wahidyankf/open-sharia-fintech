# Gherkin Acceptance Criteria — Journey Coherence

Every scenario requires an explicit `When` and `Then`. Prefer `And`/`But` when a step simply
continues the previous semantic phase, but do not impose a one-primary-keyword cardinality rule.

Repeat `Given`, `When`, or `Then` when the steps describe one continuous user journey. Split a
scenario only when its actions/outcomes are independently meaningful or unrelated. Never rewrite
an existing coherent journey solely for keyword uniformity.

Scenario Outline rows expand into separate executable scenarios. Each expanded scenario must map
to Unit and every applicable higher-layer adapter under the
[BDD standard](../../../../repo-governance/development/behaviour-driven-development.md).

```gherkin
Scenario: Complete a two-step recovery journey
  Given a member has an expired session
  When the member requests a recovery code
  Then the request is recorded
  When the member submits the valid code
  Then the session is restored
```
