# Mandatory Systematic Probes, URL Naturalness, and Responsive Usability

## Mandatory Systematic Probes (Forcing Functions)

The dimensions checklist gives breadth; these four named probes force the specific
first-time-comprehension failures a heuristic sweep tends to **read past** — because the evaluator,
having already explored the page, stops perceiving them as a newcomer would. Run all four every
`standard`/`thorough` pass, **enumerate** the elements each targets (do not judge a sample), and
record them in the coverage map.

### A. Conditional / hidden-control discoverability

For every control that only **appears** (or only **enables**) after a prerequisite — a toggle that
shows once a quantity is non-zero, a field gated behind a selection, a button disabled until a step
completes — judge whether a first-time user could know it exists before meeting the prerequisite. A
control simply absent with no hint, or disabled with no explanation of what unlocks it, is a finding
citing **Heuristic 6 (Recognition rather than Recall)** and NN/g **Progressive Disclosure** (the path
to a gated feature must be visibly signalled, else users assume it does not exist). Expected: a
ghost/disabled affordance, helper text, or tooltip naming the prerequisite.

> Class this catches: _the school-type toggle that was simply hidden until a school-age child was
> added._

### B. Per-label jargon / real-world-match scan

Enumerate every visible control label, column header, button, and section title. For each, ask
whether a first-time user with no domain knowledge would understand it. Internal/domain jargon with
no plain-language gloss is a finding citing **Heuristic 2 (Match between system and the real
world)**. Expected: plain language, or an adjacent tooltip/help text decoding the term.

> Class this catches: _a baseline-source option labelled "Reference role" with no hint of what it
> means._

### C. Cross-view information-redundancy probe

When the same datum or panel is rendered in more than one view/tab, ask whether the duplication earns
its place or merely competes for attention. Information shown in one view that is already fully
visible in another (and adds nothing there) is a finding citing **Heuristic 8 (Aesthetic &
Minimalist Design)** and **Hick's Law** (redundant data/choices inflate decision cost). Expected: each
datum has one authoritative home unless repetition demonstrably aids the task.

> Class this catches: _the per-city expense breakdown duplicated on the Cost and Savings tabs where
> the table already showed it._

### D. Input unit / currency / locale-consistency probe

For every amount/quantity input, assert a unit or currency indicator is visible **at the field** (not
only in surrounding prose), and that the unit the field accepts matches the unit the rest of the
surface **displays**. A bare amount field, or one accepting a different unit than the page shows
elsewhere, is a finding citing **Heuristic 5 (Error Prevention)**, **WCAG 2.2 SC 3.3.2 (Labels or
Instructions)**, and **Heuristic 4 (Consistency)**. Expected: an at-field unit/currency indicator or
selector consistent with the surrounding display.

> Class this catches: _a gross-salary input that silently assumed USD on a page showing local + USD
> everywhere else, with no currency selector._

## URL Naturalness (Nielsen — "URLs as UI")

The address bar is part of the interface. A natural URL helps the user orient, trust, predict, and
share; an unnatural one leaks implementation, breaks scent, and resists guessing. Evaluate the URL(s)
under test and a sample of the link graph against:

- **Readable & meaningful** — human words, not opaque IDs; lowercase kebab-case; no
  `%20`/encoded spaces; no `.php`/`.aspx`/`.jsp` implementation extensions.
- **Predictable & guessable** — the path hierarchy mirrors the site's information architecture and
  the on-page breadcrumb; a user could guess a sibling URL.
- **Matches content (scent)** — the slug describes what the page actually shows; no mismatch
  between the URL and the rendered title/H1.
- **No cruft or leakage** — primary content is not addressed by `?id=8472` query soup, session IDs,
  tracking params as the canonical URL, or deep auto-generated hashes; navigation state that should
  be bookmarkable lives in a clean path/param, not a fragment the user can't predict.
- **Hackable / shortenable** — removing a trailing path segment lands on a sensible parent, not a 404.
- **Consistent** — locale prefix (`/en/`, `/id/`), trailing-slash policy, and casing are uniform
  across the site; sibling pages follow one URL pattern.
- **Reasonable length & depth** — not needlessly deep or long; the meaningful part is near the
  front.

A URL that is confusing, unpredictable, leaky, or inconsistent is a finding citing Heuristic 4
(consistency/standards) and information scent — the URL failed to predict or match its content.

## Responsive Usability (mobile / tablet / desktop)

Responsiveness here is judged as **usability at each size**, not merely "does the layout not break"
(that layout-defect angle is `web-exploratory-tester`'s). At mobile (375, plus 320 reflow), tablet
(768), and desktop (1280, plus 1440 when `thorough`), and in each locale, evaluate:

- **Predictable transformation** — when nav collapses to a hamburger or columns restack, can a
  first-time user still find and predict where things went? Is the collapsed nav discoverable and
  labelled?
- **Content & function parity** — no feature, link, or information silently disappears at a smaller
  size; the same task is completable on mobile as on desktop (a divergence here is also a
  behavioural-consistency concern — record which size is the odd one out).
- **Touch ergonomics** — targets are reachable and large enough (Fitts's Law; WCAG 2.5.8); primary
  actions sit within comfortable thumb reach; tap targets are not crowded.
- **Readability & flow** — text remains legible without horizontal scroll; reading order and
  grouping survive the restack (Law of Proximity); tables/wide content degrade gracefully to a usable
  form.
- **Consistency across sizes** — terminology, labels, and the same datum agree across breakpoints;
  only _intended_ responsive differences differ. (This is exactly the class of bug where a desktop
  table and a mobile card show different values — judge it from the naive user's seat: which one do
  they trust?)

Capture a screenshot per breakpoint/locale for the evidence trail, saved to the backlog plan's
`evidence/` subfolder (named `phase-N-<description>-<locale>-<breakpoint>px.png` per the
[Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md)),
not `local-temp/` — cited screenshots are committed proof.
