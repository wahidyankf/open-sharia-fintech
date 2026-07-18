# E2E Coverage: Rule/Feature-Level Skip/Fixme Gap

## Context

`apps/rhino-cli/src/application/e2e_coverage/parser.rs`'s `scan_skip_or_fixme_describe_titles`
detects a `Scenario Outline`-level `@skip`/`@fixme` first-class playwright-bdd tag (a
`test.describe.skip(...)`/`.fixme(...)` wrapping the Outline's Examples-row tests, whose own nested
leaf `test(...)` calls remain plain and unsuffixed). playwright-bdd's `renderDescribe` — the code path
that produces this wrapping shape — is not Outline-specific: it is the SAME mechanism used for
`Rule:`-level and `Feature:`-level tags (`node_modules/playwright-bdd/dist/generate/file.js:153-160`).
A `Rule:`-level `@skip`/`@fixme` tag on a `.feature` file that also has other, non-skipped content
produces the identical shape one AST level up — and `scan_skip_or_fixme_describe_titles`, scoped to
Outline-level only, does not see it. The nested scenario titles land in `rendered` (via the ordinary
`bound_test_title_re` match) but never in `unbound`, so `is_unbound_or_absent` reports them as
covered even though Playwright never executes them at runtime (the parent `.skip()`/`.fixme()`
disables all children).

## Origin

Surfaced during `plans/done/2026-07-18__e2e-scenario-coverage-gap-detector`'s PR #66 cycle-7 (final,
hard-capped) `pr-review-maker` pass — 2 MEDIUM findings, confirmed dormant (zero `.feature` files in
this repo use `@skip`/`@fixme`/`@only` today) but structurally real. Deferred per the user's explicit
"cap total review cycles at 7, document cycle-7 findings but do not act on them further" decision.
Filed per the
[Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
code-routing rule.

## Scope

**In scope:**

- Extend `scan_skip_or_fixme_describe_titles` (or add a sibling function) to also detect a
  `Rule:`-level or `Feature:`-level `@skip`/`@fixme` wrapping `describe` block, folding its nested
  scenarios into the `unbound` set the same way the Outline-level case already does.
- Refresh `tech-docs.md` DD-6 in the (now-archived)
  `plans/done/2026-07-18__e2e-scenario-coverage-gap-detector/tech-docs.md` — actually, since that
  plan is archived, the doc-refresh instead updates whichever durable doc now documents the shipped
  `e2e-coverage` design (see Tech Docs task in delivery.md — locate the correct current home before
  writing).
- A regression fixture: a `.feature` file using `Rule:` with a `@skip` or `@fixme` tag plus other
  non-skipped content, wired into one of the 11 playwright-bdd e2e projects (or a dedicated test
  fixture project) to prove the gate now catches it.

**Out of scope:**

- Any other e2e-coverage detection gap not identified by cycle-7's review.
- `.only`-suffixed suites (deliberately excluded — genuinely executes, not a gap).

## Document Navigation

- [brd.md](./brd.md)
- [prd.md](./prd.md)
- [tech-docs.md](./tech-docs.md)
- [delivery.md](./delivery.md)

## Related

- [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
- PR #66 (`ose-public`) cycle-7 review comments (`apps/rhino-cli/src/application/e2e_coverage/parser.rs:136`
  and `tech-docs.md:169` in the archived plan) — full technical verification against
  `node_modules/playwright-bdd/dist/**` source is recorded there.
