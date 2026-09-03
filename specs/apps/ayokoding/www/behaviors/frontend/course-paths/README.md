# course-paths — ayokoding-www Gherkin Domain

Behaviour scenarios for the learning-path schema, prerequisite DAG, and path-aware navigation
mechanism built by `ayokoding-learning-path-02-schema-and-prerequisite-dag`.

`ayokoding-learning-path-03-navigation-ui` (Phases 2-5) step-bound every scenario in this domain
whose owning UI now exists: 19 of the 24 scenarios below, across 15 of the 18 feature files —
`@unit` for every one of them, plus `@e2e` for whichever of Phase 3's two Playwright step files
(`apps/ayokoding-www-fe-e2e/tests/e2e/steps/course-paths.steps.ts` for 14 scenarios;
`apps/ayokoding-www-fe-e2e/tests/e2e/steps/course-paths-a11y.steps.ts` for the accessibility scenario)
also binds each one. 5 scenarios across 4 feature files remain genuinely `@wip`:

- **[build-green.feature](./build-green.feature)** — the full path-navigation feature set's
  build-green composite check doesn't exist yet.
- **[manifest-integrity.feature](./manifest-integrity.feature)** — deferred to the downstream
  manifests plan that will publish real manifest data (`manifests/` stays empty until then, so
  there is no real manifest set to check integrity against yet).
- **[prerequisite-consistent-ordering.feature](./prerequisite-consistent-ordering.feature)**'s two
  scenarios — same downstream-manifests dependency as above.
- **[breadcrumb.feature](./breadcrumb.feature)**'s "A legacy fundamentally-strong URL redirects to
  the canonical course URL" — its base redirect is already shipped and step-bound by the archived
  `ayokoding-learning-path-01-url-restructure`
  (`specs/apps/ayokoding/www/behaviors/frontend/navigation/course-rehome-redirects.feature`,
  `@unit @e2e`); only the "redirect preserves path context" clause is unowned — that plan is closed
  and will not reopen, and this plan's `prd.md` disclaims owning the scenario itself.

`@wip` is the behavior-coverage validator's own step-binding-deferral exemption:
`apps/rhino-cli/src/application/behavior_coverage/validator.rs` documents and implements "`@wip`
scenarios are fully exempt". See `<PLAN>/evidence/phase-2-specs-coverage-delta.txt` for the Phase 2
deferral reasoning that originally applied to every scenario this PR has since un-`@wip`'d.

## Feature Files

- **[path-order-nav.feature](./path-order-nav.feature)** — Prev/next and the path rail follow the
  active path's manifest order, at desktop and phone widths (3 scenarios: 1 `@unit`, 2 `@unit @e2e`)
- **[omitted-course.feature](./omitted-course.feature)** — A course a path's manifest omits renders
  its canonical view instead of that path's nav (1 scenario, `@unit @e2e`)
- **[canonical-fallback.feature](./canonical-fallback.feature)** — A course renders its full
  canonical view whenever no path context applies (2 scenarios, `@unit @e2e`)
- **[invalid-path-fallback.feature](./invalid-path-fallback.feature)** — An unrecognized path
  context falls back to the canonical view without an error (1 scenario, `@unit @e2e`)
- **[breadcrumb.feature](./breadcrumb.feature)** — The path landing page, breadcrumb, and legacy
  URL redirect all carry and honour path context (3 scenarios: 1 `@unit @e2e`, 1 `@unit`, 1 `@wip`)
- **[manifest-integrity.feature](./manifest-integrity.feature)** — Every manifest course reference
  resolves to a real, unique course (1 scenario, `@wip`)
- **[prerequisite-display.feature](./prerequisite-display.feature)** — A course page lists its
  declared prerequisites regardless of path context (1 scenario, `@unit`)
- **[prerequisite-consistent-ordering.feature](./prerequisite-consistent-ordering.feature)** —
  Prerequisite ordering is enforced without requiring prerequisite completeness (OI-4 link-don't-walk
  ruling) (2 scenarios, `@wip`)
- **[landing-hero.feature](./landing-hero.feature)** — The path landing hero states the path's
  promise above the fold (1 scenario, `@unit @e2e`)
- **[skills-path-landing-body.feature](./skills-path-landing-body.feature)** — A skills path landing
  renders its ramp body content (1 scenario, `@unit @e2e`)
- **[accessibility.feature](./accessibility.feature)** — Path navigation affordances meet the
  platform's accessibility bar (1 scenario, `@unit @e2e`)
- **[build-green.feature](./build-green.feature)** — The full path navigation feature set builds and
  tests green together (1 scenario, `@wip`)
- **[paths-hub-category-grouping.feature](./paths-hub-category-grouping.feature)** — The paths hub
  groups paths by category instead of a flat grid (1 scenario, `@unit @e2e`)
- **[category-landing-arc-chooser.feature](./category-landing-arc-chooser.feature)** — The careers
  category landing offers an arc chooser (1 scenario, `@unit @e2e`)
- **[skills-fixed-arc-statement.feature](./skills-fixed-arc-statement.feature)** — The skills
  category landing states its one fixed arc with no chooser (1 scenario, `@unit @e2e`)
- **[category-landing-empty-state.feature](./category-landing-empty-state.feature)** — A category or
  arc landing with no published manifests renders an explicit empty state (1 scenario, `@unit`)
- **[arc-landing-two-role.feature](./arc-landing-two-role.feature)** — An arc landing with two roles
  renders both cards fully, without a placeholder (1 scenario, `@unit @e2e`)
- **[arc-landing-one-role.feature](./arc-landing-one-role.feature)** — An arc landing with one role
  renders a full card, not a sparse stub (1 scenario, `@unit @e2e`)

## Conventions

- **File naming**: `[behaviour].feature` (kebab-case)
- **Step language**: UI-semantic or resolver-semantic, matching the scenario's owning plan
- **User story block**: Every `Feature:` block opens with `As a … / I want … / So that …`
- **Tagging**: `@unit` scenarios are step-bound and covered by
  `nx run ayokoding-www:specs:behavior:coverage`; `@e2e` is added only once a Playwright binding
  exists (`nx run ayokoding-www-fe-e2e:specs:e2e:coverage` gates on it separately — adding the tag
  before the binding exists fails that gate); `@wip` scenarios are exempt from step-binding until
  their owning phase/plan implements the underlying UI

## Related

- [Parent surface README](../../README.md)
- [Domain gherkin index](../README.md)
