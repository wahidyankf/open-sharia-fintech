# BRD: Resizable Docs Sidebar (ayokoding-www)

## Business Goal

Give ayokoding.com readers control over the docs navigation column width so the site adapts to
their content depth and screen, and — as a second-order benefit — establish a reusable resizable
panel primitive in the shared design system (`libs/web-ui`) that future apps can adopt without
re-solving drag/keyboard/persistence mechanics.

## Business Rationale (WHY)

The docs sidebar is a fixed 250 px column [Repo-grounded:
`apps/ayokoding-www/src/app/[locale]/(content)/layout.tsx:13`]. AyoKoding's content tree is deep and
its labels can be long; a fixed width forces two bad outcomes:

- On large screens, readers cannot widen the rail to read truncated/nested labels without opening
  each section.
- On smaller `md`-range screens, readers cannot narrow the rail to reclaim reading width.

Letting the reader set — and keep — their preferred width is a low-risk, high-familiarity
ergonomics win (the interaction is a standard docs-site convention). Extracting the mechanic into
`libs/web-ui` avoids a one-off implementation and pays forward to the other web apps.

## Business Impact

**Pain points addressed**:

- Truncated navigation labels with no reader remedy.
- No way to trade sidebar width for reading width per reader preference.
- Absence of a shared resizable primitive means each future app would re-implement drag + keyboard +
  persistence from scratch.

**Expected benefits** [Judgment call — qualitative reasoning, not a measured KPI]:

- Improved reading ergonomics on the docs surface (reader sets width once; it persists).
- A durable, tested `libs/web-ui` primitive reduces future per-app cost for the same interaction.
- Keyboard-operable resize keeps the surface WCAG AA compliant, consistent with the repo's
  Accessibility First principle.

## Business-Level Success Metrics

- **Observable fact**: the docs `<aside>` width is adjustable by drag and by keyboard, and the value
  survives a full page reload and a new browser session (verifiable via the acceptance scenarios in
  `prd.md` and the E2E/Playwright evidence in `delivery.md`).
- **Observable fact**: the `resizable-panel` primitive is exported from `libs/web-ui` and covered by
  unit tests, a Storybook story, and `specs/libs/web-ui` Gherkin (verifiable via the quality gates in
  `delivery.md`).
- No numeric engagement/retention target is claimed — this is a solo-maintainer ergonomics change,
  not an instrumented growth experiment. [Judgment call]

## Affected Roles

Solo-maintainer repo — the maintainer wears the design-system-owner hat (for the `libs/web-ui`
primitive) and the ayokoding-www-app-owner hat (for the consumption + mobile preset). Consuming
agents: `swe-ui-maker` / `swe-ui-checker` / `swe-ui-fixer` (primitive + app UI), `swe-typescript-dev`
(core/hook logic + tests), `specs-maker` (Gherkin), the deployer for `ayokoding-www`. No sign-off
ceremony.

## Business-Scope Non-Goals

- **No SSR/cookie-based width.** The initial server render uses the default width; the persisted
  width applies after hydration. A brief first-paint at the default width is accepted in exchange
  for zero server plumbing. (Persistence via `localStorage`, matching `theme-toggle.tsx`.)
- **No multi-pane split-view group.** The primitive is a single collapsible side rail, not a
  general N-pane resizable group.
- **No visual redesign** of the sidebar tree, nor any change to the content/navigation data model.
- **No rollout to other apps** in this plan — the primitive merely makes future adoption cheap.

## Business Risks and Mitigations

| Risk                                                                 | Likelihood | Mitigation                                                                                                               |
| -------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| Hand-rolling drag/keyboard resize introduces subtle interaction bugs | Medium     | Full unit + `vitest-axe` + E2E coverage; zero new packages added (DD-2 mandated, runtime AND dev), keeping surface small |
| Hydration mismatch from reading `localStorage` during render         | Medium     | Read persisted width in an effect after mount (mirror `theme-toggle.tsx`); render default width on the server            |
| Keyboard/drag resize regresses accessibility                         | Low        | `role="separator"` + `aria-orientation` + `aria-valuenow/min/max`; covered by `vitest-axe` and E2E keyboard test         |
| Layout shift/CLS from persisted width on large content pages         | Low        | Clamp to a relative range (15%–35% vw) so content column stays usable; horizontal scroll absorbs overflow                |
| Primitive over-generalized before a second consumer exists           | Low        | Keep the primitive minimal (single side rail); defer multi-pane group per Simplicity Over Complexity                     |

## References

- [Accessibility First principle](../../../repo-governance/principles/content/accessibility-first.md)
- [Feature Change Completeness](../../../repo-governance/development/quality/feature-change-completeness.md)
