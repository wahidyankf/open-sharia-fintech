# Mandatory Systematic Probes, Part 2: Probe D, and URL Naturalness

## D. Input unit / currency / locale-consistency probe

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
