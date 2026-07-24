# course-paths — ayokoding-www Gherkin Domain

Behaviour scenarios for the learning-path schema, prerequisite DAG, and path-aware navigation
mechanism built by `ayokoding-learning-path-02-schema-and-prerequisite-dag`.

**Every scenario in this domain is tagged `@wip` and carries no level tag.** The pure resolvers
this plan ships (`resolvePathNav`, `parsePathContext`, `resolvePrerequisites`,
`checkPrerequisiteConsistency`, `checkManifestIntegrity`) are the mechanism behind these scenarios,
but the step bindings that make them executable belong to a downstream plan —
`ayokoding-learning-path-03-navigation-ui` for most scenarios, and
`ayokoding-learning-path-01-url-restructure` for the legacy-redirect scenario in
[breadcrumb.feature](./breadcrumb.feature). `@wip` is the behavior-coverage validator's own
step-binding-deferral exemption: `apps/rhino-cli/src/application/behavior_coverage/validator.rs`
documents and implements "`@wip` scenarios are fully exempt". See
`<PLAN>/evidence/phase-2-specs-coverage-delta.txt` for the recorded deferral and its closing plan.

## Feature Files

- **[path-order-nav.feature](./path-order-nav.feature)** — Prev/next and the path rail follow the
  active path's manifest order, at desktop and phone widths (3 scenarios)
- **[omitted-course.feature](./omitted-course.feature)** — A course a path's manifest omits renders
  its canonical view instead of that path's nav (1 scenario)
- **[canonical-fallback.feature](./canonical-fallback.feature)** — A course renders its full
  canonical view whenever no path context applies (2 scenarios)
- **[invalid-path-fallback.feature](./invalid-path-fallback.feature)** — An unrecognized path
  context falls back to the canonical view without an error (1 scenario)
- **[breadcrumb.feature](./breadcrumb.feature)** — The path landing page, breadcrumb, and legacy
  URL redirect all carry and honour path context (3 scenarios)
- **[manifest-integrity.feature](./manifest-integrity.feature)** — Every manifest course reference
  resolves to a real, unique course (1 scenario)
- **[prerequisite-display.feature](./prerequisite-display.feature)** — A course page lists its
  declared prerequisites regardless of path context (1 scenario)
- **[prerequisite-consistent-ordering.feature](./prerequisite-consistent-ordering.feature)** —
  Prerequisite ordering is enforced without requiring prerequisite completeness (OI-4 link-don't-walk
  ruling) (2 scenarios)

## Conventions

- **File naming**: `[behaviour].feature` (kebab-case)
- **Step language**: UI-semantic or resolver-semantic, matching the scenario's owning plan
- **User story block**: Every `Feature:` block opens with `As a … / I want … / So that …`
- **Tagging**: every scenario here is `@wip` only — no `@unit`/`@integration`/`@e2e` level tag and
  no `@covers` marker exists yet

## Related

- [Parent surface README](../../README.md)
- [Domain gherkin index](../README.md)
