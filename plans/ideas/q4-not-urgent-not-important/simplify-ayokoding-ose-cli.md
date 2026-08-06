# Simplify ayokoding-cli and ose-cli

One-line summary: reduce accumulated complexity in `ayokoding-cli` and `ose-cli`, or fold what they do
into rhino-cli where it overlaps.

> Idea, added 2026-07-21 (original capture undated).

## Problem / context

`ayokoding-cli` and `ose-cli` have accumulated complexity worth trimming. **Data point:** 2 per-domain
CLIs exist alongside rhino-cli, and some of their surface may now overlap with it — but the specific
complexity is unquantified (no audit has been run yet; no baseline measured).

## Why now

rhino-cli has grown into the shared CLI backbone, so the boundary between it and the per-domain CLIs is
worth revisiting before more logic accretes in the wrong place.

## Prior art / precedents

- **Simplicity Over Complexity principle** — the repo value directly motivating trimming accreted
  CLI surface.
  [principle](../../../repo-governance/principles/general/simplicity-over-complexity.md)
- **rhino-cli byte-identity boundary** — the shared CLI backbone into which genuinely-shared
  per-domain logic would fold. [sdlc-gate-standard](../../../docs/reference/sdlc-gate-standard.md)
- **Rule of three** — the refactoring guideline for when duplicated logic across CLIs is worth
  consolidating into one place.
  [rule of three](<https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)>)

## Proposed direction (sketch)

- Audit what `ayokoding-cli` and `ose-cli` actually do today and who invokes them.
- Simplify each; fold genuinely-shared functionality into rhino-cli; retire commands that are dead or
  duplicated.

## Rough scope & non-goals

In scope: simplifying the two per-domain CLIs and de-duplicating against rhino-cli.

Out of scope (for now): rewriting rhino-cli; changing the byte-identity boundary.

## Risks & open questions

- What specifically is complex or redundant in each CLI today? (open — needs an audit; the original
  capture was a one-liner with no detail)
- Are both still actively used, or has rhino-cli already superseded parts of them? (open)

## What success looks like + promotion signal

Success: each CLI does less, more clearly, with no functionality duplicated across it and rhino-cli.
Ready to promote once an audit names the concrete complexity to remove — right now this is a direction,
not a defined change.
