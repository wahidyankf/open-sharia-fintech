# PRD: Resizable Docs Sidebar (ayokoding-www)

## Product Overview

The ayokoding-www docs surface gains a **resizable navigation rail**. On desktop/tablet (`≥ md`,
≥ 768 px) the reader drags a vertical handle on the sidebar's right edge — or focuses it and uses
arrow keys — to set the rail width within a relative band (15%–35% of the viewport). The width
persists across sessions. When a nav label or nested tree is wider than the current width, the rail
content scrolls horizontally rather than clipping or wrapping. Below `md` the sidebar remains a
`Sheet` overlay drawer (`mobile-nav.tsx`); that drawer gains a small set of fixed preset widths.

The resize mechanic lives in a new shared `libs/web-ui` primitive, `resizable-panel`, so other apps
can reuse it.

## Personas

Solo-maintainer repo — personas are the hats the maintainer wears plus consuming agents:

- **Reader (end user)** — reads AyoKoding docs; wants to tune sidebar width to content depth/screen.
- **Design-system owner** — maintains `libs/web-ui`; wants a minimal, tested, reusable primitive.
- **App owner (ayokoding-www)** — wires the primitive into the content layout and mobile drawer.
- **Consuming agents** — `swe-ui-maker`/`-checker`/`-fixer`, `swe-typescript-dev`, `specs-maker`.

## User Stories

- **US-1** — As a reader on a wide screen, I want to widen the docs sidebar so I can read long,
  nested navigation labels without opening each section.
- **US-2** — As a reader on a narrow `md`-range screen, I want to narrow the docs sidebar so I can
  reclaim reading width for the article.
- **US-3** — As a keyboard-only reader, I want to resize the sidebar with the keyboard so the control
  is operable without a pointer.
- **US-4** — As a returning reader, I want my chosen sidebar width to persist across page loads and
  sessions so I do not re-adjust it every visit.
- **US-5** — As a reader whose nav labels exceed the current width, I want the sidebar content to
  scroll horizontally so no label is clipped or awkwardly wrapped.
- **US-6** — As a reader on mobile, I want the nav drawer to offer a couple of preset widths so the
  overlay fits my screen and content.
- **US-7** — As the design-system owner, I want the resize mechanic as a reusable `libs/web-ui`
  primitive so future apps adopt it without re-implementing drag/keyboard/persistence.
- **US-8** — As the repo maintainer, I want the whole feature built with zero new external packages
  so the dependency surface (and its supply-chain/soak burden) does not grow for an ergonomics change.

## Acceptance Criteria (Gherkin)

Each scenario obeys the step-keyword cardinality HARD rule (one primary `Given`/`When`/`Then`;
extras chained with `And`/`But`).

### Core width model (pure)

```gherkin
Scenario: Clamp a requested width above the maximum
  Given a viewport width of 1000 pixels and a max of 35 percent
  When a requested sidebar width of 500 pixels is clamped
  Then the resolved width is 350 pixels
```

```gherkin
Scenario: Clamp a requested width below the minimum
  Given a viewport width of 1000 pixels and a min of 15 percent
  When a requested sidebar width of 80 pixels is clamped
  Then the resolved width is 150 pixels
```

```gherkin
Scenario: Keep a requested width already inside the band
  Given a viewport width of 1000 pixels with a 15 to 35 percent band
  When a requested sidebar width of 250 pixels is clamped
  Then the resolved width is 250 pixels
```

```gherkin
Scenario: Reject an unparseable persisted value
  Given a persisted sidebar-width string of "not-a-number"
  When the persisted value is parsed
  Then the parser returns no width
  And the caller falls back to the default width
```

### Primitive — drag resize

```gherkin
Scenario: Widen the panel by dragging the handle right
  Given a resizable panel rendered at 250 pixels with a 150 to 350 pixel band
  When the user drags the separator handle 60 pixels to the right
  Then the panel width becomes 310 pixels
```

```gherkin
Scenario: Dragging past the maximum stops at the maximum
  Given a resizable panel rendered at 340 pixels with a 150 to 350 pixel band
  When the user drags the separator handle 100 pixels to the right
  Then the panel width stops at 350 pixels
```

### Primitive — keyboard resize and a11y

```gherkin
Scenario: Widen the panel with the ArrowRight key
  Given the separator handle is focused on a panel at 250 pixels
  When the user presses ArrowRight
  Then the panel width increases by the keyboard step
  And the handle exposes the new width via aria-valuenow
```

```gherkin
Scenario: The handle exposes separator semantics
  Given a resizable panel is rendered
  When the accessibility tree is inspected
  Then the handle has role "separator"
  And the handle has aria-orientation "vertical"
```

### ayokoding-www consumption — persistence, scope, horizontal scroll

```gherkin
Scenario: Persist the chosen width across a reload
  Given the reader has resized the docs sidebar to 320 pixels on a desktop viewport
  When the reader reloads the page
  Then the docs sidebar renders at 320 pixels
```

```gherkin
Scenario: Hide the resizable rail below the md breakpoint
  Given the docs page is open at a 375 pixel viewport
  When the layout renders
  Then the resizable aside is not displayed
  And navigation is available through the mobile drawer
```

```gherkin
Scenario: Scroll the sidebar horizontally when a label overflows
  Given a docs sidebar narrowed to 150 pixels containing a nav label wider than 150 pixels
  When the reader views the sidebar
  Then the sidebar content area is horizontally scrollable
  And the label is not clipped or wrapped
```

### Mobile drawer preset widths

```gherkin
Scenario: Apply a preset width to the mobile nav drawer
  Given the mobile nav drawer is open at a 375 pixel viewport
  When the reader selects the wider preset
  Then the drawer renders at the wider preset width
```

### Zero new dependencies (US-8)

```gherkin
Scenario: Ship the feature without adding any external package
  Given the plan's changes are staged for the PR
  When package.json, libs/web-ui/package.json, apps/ayokoding-www/package.json, and package-lock.json are diffed against origin/main
  Then no dependency or devDependency key is added in any of the three package.json files
  And package-lock.json introduces no new external package
```

## UI-Design-Funnel

> This plan is **UI-bearing** (adds a `libs/web-ui` component and changes `apps/ayokoding-www`
> screens). Per the UI Mockups in Plan Docs convention, the funnel below documents diverge → narrow
> → select → justify. Low-fidelity ASCII wireframes are inline; the two high-fidelity
> `.excalidraw.png` finalists are produced during delivery (Phase 1) and saved under
> `./assets/`, then embedded here.

### R5 grounding note (survey existing UI before drafting)

Before drafting, survey and reuse:

- `libs/web-ui/src/primitives/` [Repo-grounded] — existing primitives (`separator`, `scroll-area`,
  `sheet`, `tabs`, …) follow a `radix-ui` + `cn` + CVA pattern with `data-slot` attributes
  (see `scroll-area.tsx`). The new `resizable-panel` MUST match this pattern and reuse tokens.
- `apps/ayokoding-www/src/app/[locale]/(content)/layout.tsx` [Repo-grounded] — the current fixed
  `<aside>` shell (sticky, `overflow-y-auto`, `border-r border-border`) is the layout to preserve.
- `apps/ayokoding-www/src/features/navigation/shell/sidebar-tree.tsx` [Repo-grounded] — the tree
  content whose container gains `overflow-x-auto`.
- `libs/web-ui/src/components/theme-toggle/theme-toggle.tsx` [Repo-grounded] — the raw `localStorage`
  persistence pattern to mirror for the width value.

**Net-new component**: `resizable-panel` (primitive). No existing primitive provides a draggable
separator; `separator` is decorative only. Reference the `swe-developing-frontend-ui` skill during
implementation.

### R7 prior-art citation

**Prior-art findings** (Phase 1 `web-researcher` survey, 2026-07-15):

- **VS Code Side Bar** — drag resize uses VS Code's internal "sash" widget, and layout (including
  sizes) persists across sessions per official docs (`[Verified]`,
  [code.visualstudio.com/docs/configure/custom-layout](https://code.visualstudio.com/docs/configure/custom-layout)).
  Keyboard resize exists for the primary Side Bar via `workbench.action.increaseViewSize`/
  `decreaseViewSize` but ships with **no default keybinding** (`[Needs Verification]`,
  community-sourced); the newer secondary/auxiliary sidebar has no keyboard-resize path at all — a
  2026 feature request for it was closed "not planned" (`[Verified]`,
  [microsoft/vscode#300121](https://github.com/microsoft/vscode/issues/300121)). This plan's
  default-functional keyboard handle improves on VS Code's own inconsistent story.
- **Docusaurus and Nextra** — **neither ships a resizable sidebar** (`[Verified]`, negative
  finding). Docusaurus exposes only a static `--doc-sidebar-width` CSS variable (default 300px) and
  has an open, unshipped feature request
  ([docusaurus.io/feature-requests/p/make-sidebar-width-resizable-in-gui](https://docusaurus.io/feature-requests/p/make-sidebar-width-resizable-in-gui));
  community guidance in
  [facebook/docusaurus#9676](https://github.com/facebook/docusaurus/discussions/9676) recommends a
  fully custom drag-divider implementation. Nextra's official Layout docs
  ([nextra.site/docs/docs-theme/built-ins/layout](https://nextra.site/docs/docs-theme/built-ins/layout))
  document only collapse-level and visibility props, no width control. This confirms building
  `resizable-panel` as a first-class `libs/web-ui` primitive fills a real gap neither framework
  covers.
- **`react-resizable-panels`** — its handle (`PanelResizeHandle`, renamed `Separator` in v4.0.0)
  renders `role="separator"` plus `aria-orientation`, `aria-valuemin`/`aria-valuemax`/
  `aria-valuenow`, `aria-controls`, `aria-disabled`, and `tabIndex=0` (`[Verified]`, inspected
  directly in the shipped v4.12.2 bundle and
  [CHANGELOG.md](https://raw.githubusercontent.com/bvaughn/react-resizable-panels/main/CHANGELOG.md)/
  [README.md](https://raw.githubusercontent.com/bvaughn/react-resizable-panels/main/README.md)).
  Keyboard step is a fixed **±5** per arrow-key press on the matching axis (orthogonal-axis arrows
  are no-ops), with `Home`/`End` snapping to the min/max bound (`[Verified]`, read from
  [dist/react-resizable-panels.js](https://unpkg.com/react-resizable-panels@latest/dist/react-resizable-panels.js)).
  This confirms this plan's `role="separator"` + `aria-valuenow` + arrow-key-step design matches the
  closest external prior art's accessible contract.

**Sequencing note**: the three alternatives below and the Select/Justify decision were already
directed by the user's own explicit choices during pre-write grilling (edge-handle drag + keyboard,
`tech-docs.md` DD-1/DD-3/DD-4/DD-6/DD-7 — "per the user's decision, grill Q1–Q5c"), not invented
blind by an agent. The Phase 1 `web-researcher` survey is therefore a **confirmatory/citation-only**
pass: it grounds the already-directed design in named prior art (VS Code, Docusaurus/Nextra,
`react-resizable-panels`) and records citations for `Justify`, but it does not reopen Select. If the
survey surfaces a materially different pattern the user did not consider (e.g. a collapse-to-icon
strip), that is logged as a new candidate in a follow-up plan rather than silently revising this
plan's already-decided scope.

### Diverge — low-fidelity alternatives (≥ 2 named, genuinely different)

**Option A — Edge drag handle (thin gutter on the rail's right border)** _(Selected)_

The handle is a thin vertical strip sitting on the existing `border-r`; hover shows a `col-resize`
cursor; focus shows a ring. Minimal chrome, closest to the current layout.

```text
Desktop / tablet (>= md)                          Mobile (< md)
+-------------------+---------------------------+   +---------------------------+
| SIDEBAR       |  ||  ARTICLE CONTENT          |   | [=]  AyoKoding      [theme]|
| (nav tree)    |  ||                           |   +---------------------------+
|  > Section A  |  ||   # Page title            |   |  (article content, full   |
|    > Item 1   |  || <- handle (grab/arrows)   |   |   width; no side rail)     |
|    > Item 2   |  ||                           |   |                           |
|  > Section B  |  ||   Body text ...           |   |  Drawer (Sheet) opens over |
| [<-- overflow |  ||                           |   |  content with preset width |
|  scrolls -->] |  ||                           |   |  chooser inside header.    |
+-------------------+---------------------------+   +---------------------------+
   ^ width = 15%..35% of viewport, drag/keys      ^ preset widths, not free drag
```

**Option B — Explicit rail footer control (drag handle + a small width control in the rail footer)**

Same edge handle, plus a footer row with "narrow / default / wide" buttons and a reset. More
discoverable for non-drag users, but adds persistent chrome to every docs page and duplicates the
keyboard affordance the handle already provides.

```text
+-------------------+---------------------------+
| SIDEBAR       |  ||  ARTICLE CONTENT          |
|  > Section A  |  ||                           |
|  > Section B  |  ||                           |
|               |  ||                           |
| [narrow][def] |  ||                           |
| [wide] [reset]|  ||                           |
+-------------------+---------------------------+
   ^ extra footer control row (more chrome)
```

**Option C — Floating collapse+resize rail (overlay handle with a collapse toggle)**

The rail can fully collapse to an icon strip and expand on hover, with the drag handle only visible
on hover. Powerful but a larger behavioral change (collapse state, hover-expand) beyond this plan's
"make width adjustable" scope; more surface to test and to get wrong on touch/hybrid devices.

```text
+--+----------------------------------+        +-------------------+-------------+
|▤ |  ARTICLE (rail collapsed)        |  <-->  | SIDEBAR (expanded)|  ARTICLE    |
|▤ |                                  |        |  > Section A   |  ||           |
|▤ |                                  |        |  > Section B   |  ||           |
+--+----------------------------------+        +-------------------+-------------+
   ^ collapsed icon strip / hover-expand + drag (bigger scope)
```

### Narrow — hi-fi finalists

The two strongest alternatives carried to high fidelity as `.excalidraw.png` (produced in Phase 1):

> **Status: NOT YET PRODUCED.** Neither `.excalidraw.png` file exists yet — the two `![]()`
> references below are placeholders that will render as broken images until Phase 1 runs. This is a
> deliberately deferred-but-gated Phase 1 deliverable, not a silently missing artefact:
> `delivery.md` Phase 1's own gate (`test -f … .excalidraw.png` for both files) blocks Phase 2 from
> starting until both files exist on disk.

- **Finalist 1 — Option A (Edge drag handle)**: `![Hi-fi mockup of the edge drag-handle resizable docs sidebar on desktop and mobile](./assets/resizable-sidebar-option-a.excalidraw.png)`
- **Finalist 2 — Option B (Rail footer control)**: `![Hi-fi mockup of the resizable docs sidebar with an explicit footer width control](./assets/resizable-sidebar-option-b.excalidraw.png)`

Dropped: **Option C (Floating collapse+resize rail)** — collapse/hover-expand is a larger behavioral
change than "adjustable width" and risks touch/hybrid regressions; out of scope for this plan.

### Select

**Selected: Option A — Edge drag handle.** It delivers drag + keyboard resize with the least new
chrome, preserves the current layout (`border-r`, sticky, `overflow-y`), and maps cleanly onto a
minimal `resizable-panel` primitive. The keyboard-operable `role="separator"` handle satisfies the
non-drag/accessibility need that Option B's footer buttons were meant to cover, so Option B's extra
chrome is unnecessary.

### Justify — decision record

| Design                         | Outcome    | Why                                                                                                                |
| ------------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| Option A — Edge drag handle    | **Winner** | Minimal chrome; preserves current layout; keyboard `separator` handle covers the non-drag path; smallest primitive |
| Option B — Rail footer control | Runner-up  | Discoverable, but adds persistent chrome to every docs page and duplicates the handle's keyboard affordance        |
| Option C — Floating collapse   | Dropped    | Collapse/hover-expand exceeds "adjustable width" scope; touch/hybrid regression surface too large for this plan    |

### Responsive strategy (mobile-first, per breakpoint)

- **Mobile (`< md`, < 768 px)**: no resizable rail. Navigation is the existing `Sheet` overlay
  drawer (`mobile-nav.tsx`), which reflows from the side-rail column into a full-height left sheet.
  The drawer offers **fixed preset widths** (e.g. a default and a wider preset) — no free drag,
  since an overlay drawer does not compete with content width the way a persistent column does.
- **Tablet (`md`, ≥ 768 px)**: the resizable `<aside>` appears (`md:block`) and is fully
  drag + keyboard resizable within the 15%–35% band. This is the lower edge of the resizable range.
- **Desktop (`lg`, ≥ 1024 px)**: identical resizable behavior; the relative 15%–35% band means the
  usable pixel range scales up with the viewport, so ultra-wide screens get a proportionally wider
  allowable rail without a hard pixel cap.
- **Reflow summary**: side rail (≥ md) → overlay sheet with preset widths (< md). The article
  content column is `min-w-0 flex-1` so it always absorbs the remaining space; sidebar content uses
  `overflow-x-auto` at every breakpoint so narrow widths never clip labels.

## Product Scope

**In-scope features**: drag resize, keyboard resize, width persistence, relative min/max clamp,
horizontal scroll of nav content, mobile preset widths, reusable `resizable-panel` primitive with
story + tests + specs. **Hard constraint**: everything is built with ZERO new external packages
(runtime or dev) — React, the existing `libs/web-ui` primitives/tokens, the existing Radix/CVA
deps, and the existing test tooling only (see `tech-docs.md` DD-2).

**Out-of-scope features**: SSR/cookie width, multi-pane split group, sidebar visual redesign,
collapse-to-icon-strip behavior, wiring the primitive into any other app.

## Product Risks

- **Hydration flash** at the default width before `localStorage` applies — accepted; mitigated by
  effect-based read (see `tech-docs.md`).
- **Touch drag ergonomics** on hybrid `md` tablets — the handle must have an adequate hit area;
  covered by the Storybook a11y check and E2E.
- **Persisted width becomes invalid** if the viewport shrinks (e.g. window resize) — the clamp is
  re-applied against the current viewport so a stored 35%-of-wide value is re-clamped on a narrow
  screen.
