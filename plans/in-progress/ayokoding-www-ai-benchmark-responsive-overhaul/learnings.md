<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: ayokoding-www-ai-benchmark-responsive-overhaul

## Learning: breakpoint verification that checks presence, not legibility, passes a broken chart

- **Context**: seeded at plan-authoring time from the diagnosis of the prior plan's sign-off
  evidence. The merged-chart plan recorded "pass at 320/375/768/1280/1440px for both locales — no
  content/... issue" (`plans/done/2026-07-30__ayokoding-www-ai-benchmark-merged-chart/delivery.md`
  line 1392) and merged on that basis.
- **Observation**: every element genuinely WAS present at 320px. Several were rendering at 4.3 CSS
  px. Presence and legibility are independent properties, and a screenshot scaled into a review pane
  hides a factor-of-two type-size error.
- **Why it might generalize**: any plan whose responsive verification asserts element presence per
  breakpoint inherits the same blind spot. A durable fix would require responsive verification to
  read a computed style or a bounding box — not merely to confirm the element exists. Candidate
  homes: `repo-governance/development/quality/manual-behavioral-verification.md`,
  `repo-governance/development/quality/evidence-capture.md`.

## Learning: a "same DOM at every breakpoint" responsive strategy is incompatible with stable typography inside a scaled coordinate system

- **Context**: the prior plan chose identical-DOM-at-every-breakpoint as its responsive strategy and
  recorded it as a deliberate simplification.
- **Observation**: combined with an SVG `viewBox`, identical-DOM makes uniform scale the only
  responsive lever available, which forces typography to be a function of viewport width. The two
  properties are mutually exclusive by construction, not merely in tension.
- **Why it might generalize**: this is a design-review heuristic — "identical DOM at every
  breakpoint" should trigger the follow-up question "then what is the responsive lever, and does it
  scale text?" Candidate home:
  `repo-governance/conventions/formatting/diagrams.md` §UI Mockups in Plan Docs, or the
  `swe-developing-frontend-ui` skill.

## Learning: collapsing a dense region hides its density rather than fixing it

- **Context**: seeded at plan-amendment time. DD-28 answered the "wall of text" report by collapsing
  the roster card from ~415px to ~110px behind a `<details>`. Shown the live card afterwards, the
  user still reported it "too cramped" and "hard to read" — because the screenshot was of the
  EXPANDED state, whose typography, per-field line count, grouping, and absent-figure handling
  DD-28 never specified. DD-34 was added to cover exactly that.
- **Observation**: length and density are independent properties of the same region, and a
  disclosure changes only the first. A collapse fix relocates the problem to whoever opens the
  disclosure, which is precisely the reader who wanted the detail.
- **Why it might generalize**: any plan answering a density complaint with progressive disclosure
  should be asked "and what does the revealed content look like?" as a matter of course. Candidate
  homes: `repo-governance/development/quality/user-facing-delivery-hardening.md`, or the
  `swe-developing-frontend-ui` skill.

## Learning: an amendment's numeric sweep must cover advisory prose, not only machine-checked gates

- **Context**: the DD-34 amendment changed several counts (3→4 funnel selections, 6→8 mockups,
  +12→+16 scenarios, 16→18 screenshots, 2→4 i18n keys). Two consecutive plan-quality-gate iterations
  (8 and 9) each found a DIFFERENT surviving stale count — Phase 2's Pause Safety prose, then
  `tech-docs.md`'s File Impact table row.
- **Observation**: the amendment correctly updated every count that a gate command greps for. What
  it missed both times was a count stated in human-readable prose or a reference table, where
  nothing mechanical reads it. The machine-checked figures were self-defending; the advisory ones
  were not.
- **Why it might generalize**: this is the "fix the class, not the sites" rule applied to counts —
  after any amendment that changes a quantity, sweep every document for that quantity rather than
  updating the places the amendment happened to touch. Candidate home:
  `repo-governance/conventions/writing/dynamic-collection-references.md`, which already forbids
  hardcoded counts of dynamic collections and could extend to intra-plan counts.

## Learning: a truncated DOM query silently under-counts, and the undercount propagates into every downstream figure

- **Context**: the plan's foundational roster size was recorded as "31 models" across `brd.md`,
  `README.md`, `prd.md`, `tech-docs.md`, and a Phase 10 baseline. The live roster has **38**. The
  error originated in the diagnosis itself: the Playwright `browser_evaluate` sweep that enumerated
  page sections used `.slice(0, 60)` to cap its output, and the model count was read off that capped
  list rather than from a `querySelectorAll(...).length`.
- **Observation**: the truncation produced a plausible number, not an obviously broken one, so
  nothing downstream looked wrong. It then propagated into per-card arithmetic, page-height
  percentages, prerender-cost math used to reject a design option, and two mockup SVGs with the
  count baked into rendered text. Plan-quality-gate iterations 1-9 all missed it; iteration 10 caught
  it only by counting the dataset directly instead of trusting the plan's own stated figure.
- **Why it might generalize**: any measurement that feeds a plan's arithmetic should be taken with a
  query whose result is a count (`.length`), never read off a list that was capped for display. More
  broadly, a checker should re-derive a plan's foundational quantities from the source of truth at
  least once rather than only checking internal consistency — every document agreeing with every
  other document is exactly what a propagated error looks like. Candidate home:
  `repo-governance/development/quality/plan-anti-hallucination.md`, as a recipe alongside the
  existing confidence-label rules.
