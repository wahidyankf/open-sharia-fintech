# Product Requirements — AI Benchmark Merged Chart

## Product overview

Replace the AI Benchmark tool's two stacked charts (capability index, token price) with one merged
chart: one row per rated model, carrying a capability bar and two price bars (input, output)
together, grouped into the same four bands (opus/sonnet/light/unrated) the page already uses, each
RATED band (opus/sonnet/light) independently sortable. **Correction (pr-review-synthesis-maker
MEDIUM finding, PR #125 fixer cycle):** the `unrated` band is never sortable — it has no composite
index to order by, renders as a plain text list, and never had a sort dropdown. An earlier
`sortUnrated` URL parameter round-tripped despite this and has been removed as dead code rather than
wired up; see `tech-docs.md`'s corrected DD-4.

## Personas

Solo-maintainer repo — these are the hats the maintainer wears, plus the consuming agents:

- **The reader** — a working engineer comparing coding-harness models, deciding which to pick for a
  task based on both capability and cost.
- **The content maintainer** — implements and reviews the merge.
- **`plan-execution`** — executes this plan's `delivery.md`.
- **`web-exploratory-tester` / `web-usability-tester` / `web-design-tester`** — Rule-15 retest
  before archival.

## User stories

**US-1**: As a reader, I want a model's capability index and its input/output price shown together
in one row, so that I can judge its value trade-off without scrolling between two chart sections.

**US-2**: As a reader, I want to re-sort a single band by price (low→high or high→low) without
losing that band's grouping, so that I can find the cheapest or most expensive model within a
capability tier I already care about.

**US-3**: As a reader, I want a sorted band's URL to be shareable, so that a link I send someone
else reproduces the same sorted view I was looking at.

**US-4**: As a reader relying on assistive technology, I want the merged chart's accessible name and
the always-visible data table to still let me reach every figure without needing to interact with
the chart at all, exactly as I can today.

## Design funnel — the merged chart

### R5 grounding note

Before drafting either tier, the following existing UI was surveyed and is reused, not
reinvented `[Repo-grounded]`:

- `shell/chart-primitives.tsx` — `Bar`, `BandGroup`, `Axis`, `TickRow`, `scaleLinear`, `bandLabel`,
  `barFillClass`/`bandInkFillClass`/`bandSwatchClass` (the WCAG-AA-audited, token-driven colour
  system) — reused unchanged by the new merged chart.
- `shell/benchmark-filters.tsx`'s `FilterSelect` — the existing native-`<select>` component already
  used for the harness/class filter bar — reused verbatim (new `id`/`label`/`options`/`onChange`
  only) for each band's new sort dropdown, so no second select-styling exists on the page.
- `shell/model-table.tsx`'s subscription-text cell pattern (`${Subscription} (${cost})`) — reused
  inline for a rated-but-subscription-only model's row (see DD-1 in `tech-docs.md`).
- `core/bands.ts`'s `computeGroups` (band grouping, roster-relative thresholds) and `core/price.ts`'s
  `lowestRate`/`rateForHarness` — both reused unchanged; the new comparators in `core/sort.ts` sort
  the SAME per-band arrays these already produce.
- No component in `libs/web-ui` was a fit for a custom SVG bar chart — the existing hand-rolled SVG
  approach (already used by both charts being replaced) is the only fit, and stays.

Net-new component: `shell/benchmark-chart.tsx` (the merged chart) and `core/sort.ts` (the three
comparators). No other net-new shell or core module.

### R7 prior-art citation

The direct, most relevant prior art is **this repository's own prior plan**
`[Repo-grounded — plans/done/2026-07-30__ayokoding-www-tools-ai-benchmark/prd.md §Diverge, accessed
2026-07-30]`, which already surveyed external comparables (Artificial Analysis Intelligence Index,
llm-stats.com, ARC Prize leaderboard, vendor pricing pages) when it built the CURRENT two-chart
page, and which additionally drafted and **rejected** a merged "Option C — Aligned Side-by-Side
Comparison Grid" for exactly the reason a naive merge risks repeating (mobile layout collapse). That
prior rejection is treated as binding prior art for this plan's own Diverge stage below — see
[`tech-docs.md` §Prior-Plan Rejection Precedent](./tech-docs.md#prior-plan-rejection-precedent) for
the full citation and why this plan's selected design avoids the same failure mode.

### Diverge — three named low-fidelity alternatives

#### Option A — Unified Stacked-Bar Rows (winner)

One row per rated model: a text line naming the model and its capability index, then three bars
stacked vertically beneath it — capability, price-in, price-out — each labelled. Bands stay grouped
exactly as today, each with its own sort control. Unrated and subscription-only-and-unrated models
keep today's plain text-list treatment (no bars at all, carried over unchanged per Q3).

```text
DESKTOP AND MOBILE (identical structure at every breakpoint — Q10)
┌──────────────────────────────────────────────────────────────────────────┐
│ AI Model Benchmark                          Data as of 2026-07-28        │
│ Harness: [ All ▾ ]   Class: [ All ▾ ]           38 of 38 models shown    │
├──────────────────────────────────────────────────────────────────────────┤
│ ── OPUS ── index ≥ 99.4 ──────────────────────  [ Sort: Capability ▾ ]   │
│ Claude Opus 5 — 94  ⚠ 55%                                                │
│   Capability  ████████████████████████████████░░           94          │
│   Price in    ██████                                        $5.00       │
│   Price out   ████████████████████                          $25.00      │
│ GPT-5.6 Sol — 99.9                                                       │
│   Capability  █████████████████████████████████░           99.9        │
│   Price in    ██████                                        $5.00       │
│   Price out   ██████████████████████████                    $30.00      │
├──────────────────────────────────────────────────────────────────────────┤
│ ── SONNET ── 85.7 ≤ index < 99.4 ──────────────  [ Sort: Price low→hi ▾ ]│
│ Claude Sonnet 5 — 85.7 ⟵ anchor                                          │
│   Capability  ████████████████████████░░░░░░░░             85.7        │
│   Price in    ███                                            $3.00       │
│   Price out   █████████████                                  $15.00      │
├──────────────────────────────────────────────────────────────────────────┤
│ ── UNRATED ── no published composite score — text list, no bars ────────│
│ MiMo v2.5 Pro · grok-build-0.1 · Gemini 3.5 Flash Lite                   │
│ Qwen3.7 Plus — Subscription ($10.00/month, OpenCode Go)                  │
├──────────────────────────────────────────────────────────────────────────┤
│ ## Full data (ModelTable, unchanged)                                     │
└──────────────────────────────────────────────────────────────────────────┘
```

A model's row scales its bars to the viewport width at every breakpoint — no separate
mobile/desktop markup branch (unlike today's two charts and `model-table.tsx`, which each render two
parallel DOM blocks toggled by CSS). A RATED model billed only by subscription (no metered rate)
shows `Subscription ($cost)` text in place of its two price bars, still inside its own row (DD-1).

#### Option B — Twin-Track Mirrored Bars

Capability bar extends rightward from a shared center spine; the price is drawn on the same row
extending leftward from the same spine — one row, one shared axis, two directions.

```text
                    ← price (USD/1M)   |   capability index →
Claude Opus 5              [$25/$5]████|████████████████████████ 94
GPT-5.6 Sol               [$30/$5]█████|█████████████████████████ 99.9
Claude Sonnet 5              [$15/$3]██|████████████████████ 85.7
```

#### Option C — Side-by-Side Columns (reprise of the prior plan's rejected Option C)

Model name, capability bar, and price bars in three adjacent columns per row, in a table-like grid.

```text
DESKTOP
┌───────────────────┬────────────────────────┬───────────────────────────────┐
│ Model             │ Capability index       │ Price USD/1M   in ▏ out       │
├───────────────────┼────────────────────────┼───────────────────────────────┤
│ Claude Opus 5     │ ███████████████ 94     │ ▏█████ 5.00  ▏████████ 25.00 │
└───────────────────┴────────────────────────┴───────────────────────────────┘
MOBILE — three columns cannot survive < 768px; they must stack, which turns
         this into Option A with an extra layout path to test and maintain —
         the SAME reason the prior plan's own Option C lost (see tech-docs.md).
```

### Narrow — the two hi-fidelity finalists

| Alternative                      | Carried to hi-fi? | Reason                                                                                                                                                        |
| -------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A — Unified Stacked-Bar Rows** | **Yes**           | Same DOM structure at every breakpoint (Q10's requirement) — no responsive layout switch needed, avoiding the prior plan's Option C failure mode entirely     |
| **B — Twin-Track Mirrored Bars** | **Yes**           | A genuinely different visual idea worth evaluating hi-fi before rejecting — see Justify below for why it lost                                                 |
| **C — Side-by-Side Columns**     | No — dropped      | Reprises the prior plan's already-rejected Option C; collapses to Option A below 768px, paying for a second layout path for a benefit that vanishes on mobile |

Hi-fi finalists:

![Option A — unified stacked-bar rows, one row per rated model with a capability bar and two price bars (input, output) stacked beneath the model name, grouped into opus, sonnet, light bands each with its own sort dropdown, unrated and subscription-only-unrated models in plain text lists beneath, at desktop width — the identical structure renders at every breakpoint](./assets/ai-benchmark-merged-option-a-stacked-rows.png)

_Option A — Unified Stacked-Bar Rows (winner). See [Select](#select) and
[Justify](#justify--decision-record) below._

![Option B — twin-track mirrored bars, capability bar extending rightward and a combined price label extending leftward from a shared center spine on the same row, annotated with two callouts explaining why the dual-direction dual-unit encoding and the collapsed price representation caused this option to lose](./assets/ai-benchmark-merged-option-b-mirrored-bars.png)

_Option B — Twin-Track Mirrored Bars (runner-up). See
[Justify](#justify--decision-record) below for why it lost._

> **Authoring note** — both tiers are committed as authored: the low-fidelity ASCII wireframes
> above, and the two hi-fidelity finalists, each hand-authored as `.svg`
> (`assets/ai-benchmark-merged-option-a-stacked-rows.svg`,
> `assets/ai-benchmark-merged-option-b-mirrored-bars.svg`) rendered via `rsvg-convert` to the `.png`
> files embedded above, per the
> [UI Mockups in Plan Docs §Both-Tiers Rule](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-both-tiers-rule.md#ui-mockups-in-plan-docs-the-both-tiers-rule).
> Colours approximate the real `--chart-band-opus`/`-sonnet`/`-light`/`-unrated` OKLCH tokens
> `[Repo-grounded — libs/web-ui-token/src/ayokoding.css, accessed 2026-07-30]` using the same
> literal-hex stand-ins the prior plan's own mockups used (`#CC78BC`, `#029E73`, `#DE8F05`,
> `#808080`) — a static image cannot reference a CSS custom property directly. Delivery Phase 1
> reuses `chart-primitives.tsx`'s already-tokenized classes directly, so the shipped page reads the
> live tokens; the mockup hex values are indicative only.

### Select

**Selected: Option A — Unified Stacked-Bar Rows.**

### Justify — decision record

| Criterion                                             | A — Unified Stacked-Bar Rows                            | B — Twin-Track Mirrored Bars                                                                          | C — Side-by-Side Columns                                        |
| ----------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Matches the stated requirement (cap+price per row)    | **Exact**                                               | Yes, but compresses input+output into one label, losing per-bar precision                             | Yes, but as a table row, not a stacked group                    |
| Responsive behaviour (Q10: same structure everywhere) | **Native — identical DOM at every breakpoint**          | Native (single row, single axis) but a narrow viewport crushes the mirrored labels illegibly          | Fails — columns cannot survive `< 768px`, must reflow to A      |
| Reader learning cost                                  | **None** — same "longer bar = more" convention as today | New — a shared bidirectional axis with two different units (index, USD) has no precedent on this page | None — reads like a table                                       |
| Bar-length-encodes-value precision (input, output)    | **Full** — three independently-scaled bars              | Reduced — one combined price segment, no separate input/output bar                                    | Full — but at the cost of the responsive failure above          |
| Implementation surface                                | **Smallest** — reuses `chart-primitives.tsx` verbatim   | Medium — needs a new bidirectional scale and center-spine layout                                      | Largest — needs a shared-axis table layout across two units     |
| SSR without client JS                                 | **Full**                                                | Full                                                                                                  | Full                                                            |
| **Verdict**                                           | **Winner**                                              | Dropped — new unlearned convention, loses per-bar price precision                                     | Dropped — reprises the prior plan's own already-rejected design |

**Why the runner-up lost**: Option B's mirrored-bar idea is visually compact, but it asks the reader
to learn a brand-new convention (two different units sharing one axis, pointing opposite
directions) that nothing else on this page — or in `chart-primitives.tsx` — uses, and it must
collapse input and output into one combined price label to fit on one shared axis, which directly
undoes Q1's decision to keep input and output as two independently-scaled bars. Option A achieves
the same "cap and price together, one glance" goal using the SAME bar convention every other chart
on this page already teaches the reader, with zero new axis semantics.

### Responsive strategy — mobile-first, per breakpoint

Per Q10 (the user's explicit follow-up), the selected design uses **the identical DOM structure at
every breakpoint** — mobile, tablet, and desktop all render the same stacked-bar row; only the
`viewBox`-scaled bar length changes with available width, exactly as `chart-primitives.tsx`'s
existing `scaleLinear` + `className="w-full"` pattern already provides for `capability-chart.tsx`
and `price-chart.tsx` today. This is a deliberate simplification versus those two charts and
`model-table.tsx`, all three of which currently render two parallel DOM blocks (mobile vs.
desktop/tablet) toggled by CSS.

| Element                      | Mobile (`< 768px`)                                                   | Tablet (`md ≥ 768px`)                                             | Desktop (`lg ≥ 1024px`)                                                                                                  |
| ---------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Model row                    | Name+index text, then 3 stacked bars — same markup as tablet/desktop | Identical markup, wider `viewBox` gives bars more horizontal room | Identical markup, widest `viewBox`; `lg`-only tick row appears (reused from `chart-primitives.tsx`'s existing `TickRow`) |
| Band header + sort dropdown  | Stacks above the band's rows, full width                             | Same, inline with band label on one row if width allows           | Same, band summary count added on the right (reused pattern from the prior plan's Option A)                              |
| Unrated / subscription lists | Plain wrapped text list, unchanged                                   | Same                                                              | Same                                                                                                                     |

**Neither the merged chart, nor its per-band sort dropdown, ever becomes horizontally scrollable or
switches to a different layout at any breakpoint.** This is the responsive strategy itself, not a
finishing touch — it is the specific property that avoids the prior plan's Option C failure mode
(see `tech-docs.md` §Prior-Plan Rejection Precedent).

## Product scope

### In scope

| #    | Feature                                                                                                                                                 |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PS-1 | One merged chart component replacing `capability-chart.tsx` + `price-chart.tsx`                                                                         |
| PS-2 | Three bars per rated model row: capability, price-in, price-out                                                                                         |
| PS-3 | Per-band sort control (Capability default / Price low→high / Price high→low), sorted by output rate (input tie-break)                                   |
| PS-4 | URL-encoded per-band sort state for the three RATED bands (`sortOpus`/`sortSonnet`/`sortLight` — `unrated` is never sortable, see the correction above) |
| PS-5 | New `core/sort.ts` pure comparator module                                                                                                               |
| PS-6 | DD-1: rated + subscription-only model renders inline `Subscription ($cost)` text in place of price bars                                                 |
| PS-7 | Rewritten + extended Gherkin in the existing `ai-benchmark.feature`                                                                                     |
| PS-8 | DD-8: harness-specific price display (AC-17/AC-18) carries over unchanged via a `harness` prop on the merged chart                                      |

### Out of scope

| #     | Feature                                                                                                                                                                                                                                   |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OOS-1 | Any change to `model-table.tsx`; no behavioral change to `benchmark-filters.tsx`'s own filter bar, other than the backward-compatible `allLabel?` widening of the shared `FilterSelect` required by the PR #125 cycle-1 sort-dropdown fix |
| OOS-2 | Any new benchmark, price, or model entering `core/data/models.ts`                                                                                                                                                                         |
| OOS-3 | Any runtime data fetch, backend, API, or database                                                                                                                                                                                         |
| OOS-4 | Any change to the harness/class URL params (`harness`, `class`)                                                                                                                                                                           |

### Product-level risks

- Rewriting 39 existing Gherkin scenarios in place risks a silent coverage gap if a scenario is
  deleted without a replacement — mitigated by `delivery.md`'s explicit scenario-count audit.
- DD-1's inline subscription-text behavior for a RATED model is a genuinely new per-row treatment
  not literally covered by the user's Q3 answer (which named the two GLOBAL list treatments) —
  flagged explicitly in the post-write grill for confirmation.

## Acceptance criteria (Gherkin)

```gherkin
Feature: AI model benchmark tool — merged capability/price chart

  Scenario: A rated model's row carries its capability bar and both price bars together
    Given a model in the sonnet band with a metered input and output rate
    When the merged chart renders that model's row
    Then the row shows one capability bar, one price-in bar, and one price-out bar
    And all three bars appear stacked within that single row, not in separate chart sections

  Scenario: Bar length is proportional to its own value
    Given a model with a composite index of 85.7 and an output rate of $15.00
    When the merged chart renders that model's row
    Then the capability bar's length is proportional to 85.7 over the composite index max
    And the price-out bar's length is proportional to $15.00 over the chart's shared price axis max

  Scenario: A band's sort control reorders only that band
    Given the sonnet band is displaying models in capability-descending order
    When the reader selects "Price: Low to High" from the sonnet band's sort control
    Then the sonnet band's rows re-render sorted by ascending output rate
    And the opus and light bands keep their own independently-selected sort order

  Scenario: A band's sort choice is encoded in the URL
    Given the reader has selected "Price: High to Low" for the opus band
    When the reader copies the current page URL
    Then the URL contains a "sortOpus" query parameter set to the descending-price value
    And loading that URL directly reproduces the opus band sorted the same way

  Scenario: An unknown sort value in the URL falls back to the default
    Given a URL containing "sortSonnet=not-a-real-value"
    When the page loads with that URL
    Then the sonnet band renders sorted by capability (the default)
    And no error is thrown

  Scenario: A rated model billed only by subscription shows inline subscription text
    Given a model in the light band with no metered rate and one subscription rate
    When the merged chart renders that model's row
    Then the row shows its capability bar as normal
    And the price-bar area of that row shows "Subscription ($cost)" text instead of two bars

  # AC-48 — added post-merge (pr-review-synthesis-maker MEDIUM finding): a rated model with no
  # reported price at all (no metered rate, no subscription, under any harness) is genuinely new
  # rendering behaviour the retired `price-chart.tsx` never had — it used to omit such models from
  # the plot entirely, so nothing rendered for them; the merged chart instead renders an inline
  # "not reported" placeholder, which had no owning scenario until now.
  Scenario: A rated model with no reported price shows a not-reported placeholder
    Given a model in the light band with no metered rate and no subscription rate
    When the merged chart renders that model's row
    Then the row shows its capability bar as normal
    And the price-bar area of that row shows a "not reported" placeholder instead of two bars

  Scenario: An unrated model still renders in the existing text-only list
    Given a model with no published composite score on any benchmark
    When the merged chart renders the roster
    Then that model appears in the unrated group's plain text list
    And no capability bar or price bar is rendered for that model

  Scenario: The merged chart keeps its accessible name and text alternative
    Given the merged chart has replaced the two former charts
    When a screen reader encounters the chart
    Then each rated band renders its own svg with role image and its own localized title as its accessible name
    And every figure the chart encodes is still reachable via the unchanged ModelTable below

  Scenario: The merged chart uses the identical DOM structure at every breakpoint
    Given the merged chart is rendered at a 375px, a 768px, and a 1280px viewport width
    When the DOM structure at each width is inspected
    Then the same set of elements renders at all three widths
    And only the pixel width of each bar changes between the three renders

  Scenario: Models are ordered identically before and after a sort change within a band
    Given the opus band is sorted by capability
    When the reader switches the opus band's sort to price low to high
    Then every model previously in the opus band still appears in the opus band
    And the set of models in the band is unchanged, only their order changes

  # AC-18 — in-place rewrite target (DD-8): matches the Gherkin scenario embedded verbatim in
  # delivery.md's Phase 2 RED step, which binds to this exact text via its `Gherkin (binds)` tag.
  # Phase 4 rewrites the existing AC-18 scenario ("A harness filter switches the price chart to
  # that harness's rate") to this text — a rewrite, not an addition, so it does not change the
  # 39 → 48 scenario-count arithmetic.
  Scenario: A harness filter switches the merged chart to that harness's rate
    Given a fixture model priced differently by two harnesses
    When the merged chart renders with that harness selected
    Then that model's price bars use that harness's own rate, not its lowest available rate
```
