# Test Dimensions Checklist (Part 1 of 2): Functional Through URL/IA Quality

Apply the dimensions relevant to the goal; record which were covered and which were not.

- **Functional flows** — every primary journey works end-to-end; state changes/navigation are
  correct; computed values are _right_ (not just present — compare to an independent calculation or
  the spec).
- **Edge cases & boundary conditions (always probe — find at least one, or state explicitly that a
  genuine attempt surfaced none)** — deliberately push past the happy path. Exercise: boundary and
  extreme values (min/max, zero, negative, very large, numeric overflow, off-by-one limits);
  empty / null / missing / whitespace-only inputs; very long strings and large datasets; special
  characters, Unicode, emoji, and RTL text; malformed or unexpected input types/formats; the
  **empty / zero-result / loading / error** state of every data view (not just the populated one);
  state-sequence edges (rapid repeat, double-submit, back/forward mid-flow, stale or concurrent
  state); and temporal edges (timezone/DST, expiry, ordering, debounce/race). A _wrong_ behaviour at
  an edge is a finding; a _correct_ edge behaviour that `specs/**` does not describe is a prime
  spec-gap candidate (see the specs-as-ground-truth reference module). This dimension is mandatory
  for every run — edge coverage is never "not applicable", only "attempted and none found" with that
  stated.
- **Behavioural consistency** — the surface must not contradict itself, even where no single spec or
  mockup is violated; an internal contradiction _is_ a defect whose "expected" cites the conflicting
  instance (the other page, state, or locale), not an external spec. (Divergence from a `specs/**`
  scenario is a spec defect instead; reserve this dimension for self-contradiction.) Probe two axes:
  - **Within the given URL** — the same action behaves the same way on repeat; identical controls
    share one behaviour; validation rules, empty/loading/error states, terminology and labels, and
    the formatting of dates / numbers / currency / units are uniform throughout the page.
  - **Across related surfaces** — the same feature, data, or component behaves consistently across
    sibling pages, locales, breakpoints (beyond intended responsive differences), and repeat visits;
    shared chrome (nav, footer, headers) and the same datum shown in two places agree.
- **Forms & validation** — required-field enforcement; field-level validation on blur and submit;
  messages are visible, descriptive, and programmatically associated (`aria-describedby`); success
  and error states behave; benign edge inputs (empty, max length, special chars, whitespace-only).
- **Navigation & links** — no 404s; external links open safely (`rel="noopener noreferrer"`);
  back/forward consistent; breadcrumbs/pagination accurate.
- **URL / IA quality** — is the address itself natural and optimal (Nielsen, "URLs as UI")? Readable
  human-meaningful slugs (lowercase kebab-case, no `.php`/`.aspx` or encoded spaces, no opaque `?id=`
  query soup or session/tracking cruft as the canonical URL for primary content); predictable and
  guessable; matches content (slug agrees with the rendered title/H1); hackable (removing a trailing
  segment lands on a sensible parent, not a 404); and consistent across the site. A leaky,
  unpredictable, or inconsistent URL is a finding.
