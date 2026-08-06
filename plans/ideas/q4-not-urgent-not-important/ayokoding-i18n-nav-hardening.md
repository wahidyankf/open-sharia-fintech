# AyoKoding i18n + Navigation Hardening

One-line summary: The `/learn` section's Indonesian locale, language switcher, top-nav wiring, and
sidebar rendering carry pre-existing defects — some CRITICAL — that a first-time or bilingual visitor
hits immediately, independent of the URL restructure that just shipped.

> Surfaced 2026-07-23 during ayokoding-learning-path-01-url-restructure execution (Phase 5 rule-15
> live-site tester triad: web-exploratory / web-usability / web-design).

## Problem / context

The Phase-5 retest against live `www.ayokoding.com` confirmed the URL restructure itself is sound, but
the spec-blind and design-aware passes surfaced defects in adjacent, pre-existing navigation and i18n
machinery the restructure never touched. Three are CRITICAL and reproduce on every attempt: (1) the
in-product language switcher 404s across the entire Learn subtree — it swaps only the locale segment
(`/en/learn` → `/id/learn`) instead of mapping to the translated slug `belajar`, so every bilingual
switch lands on "Page Not Found"; (2) the Indonesian locale at `/id/belajar` is a stale, unrelated
three-item mini-site (footer stamp "Terakhir diperbarui 16 Maret 2025") with no Courses/Paths/Legacy
counterpart at all; (3) the desktop/tablet sidebar clips the majority of course and domain labels
mid-word with no ellipsis and no visible scroll cue (measured container clientWidth 214px against
scrollWidth 299–367px — only ~58% of the widest row is painted). Two HIGH issues compound them: the
top-nav item labeled "Learn" actually navigates to `/en/browse` (a second click is required to reach
the hub), and the `id`-locale 404 page renders its error copy in English on an otherwise fully
Indonesian page.

## Why now

The restructure has drawn fresh attention and traffic to `/learn`, and old bookmarks now redirect
users into `/legacy/` URLs — so the switcher-404 and id-parity gaps are hit more often, at exactly the
moment the section is being promoted. The evidence (repro steps, measurements, screenshots) is fresh
and captured; filing now preserves it before it decays.

## Prior art / precedents

- Next.js i18n routing and localized-slug patterns —
  [Next.js internationalization docs](https://nextjs.org/docs/app/building-your-application/routing/internationalization).
- The repo's own `Accessibility First` principle (WCAG AA) —
  [accessibility-first](../../../repo-governance/principles/content/accessibility-first.md).
- The truncate-with-ellipsis-plus-title tree-navigator pattern (standard file-tree/IDE sidebars).
- The just-completed `ayokoding-learning-path-01-url-restructure` plan, whose Phase-5 retest is the
  provenance of every finding here.

## Proposed direction (sketch)

Three threads, triageable independently: route the language switcher through the same translated-slug
map the site already defines (with a graceful fallback to the locale landing page when no per-slug
translation exists) so locale switching never 404s; decide the Indonesian-locale posture — either
localize the three-bucket IA or add an honest signpost on `/id/belajar` pointing at the English
library (DD-45 already deferred `id` deliberately, so this may be WONTFIX-with-a-signpost); and give
the sidebar a working overflow contract (ellipsis + hover title, or a wider default, or a discoverable
resize grip). The top-nav "Learn" target and the `id` 404-copy localization are small, self-contained
follow-ons.

## Rough scope & non-goals

In scope: language-switcher slug mapping, id-locale posture decision, sidebar overflow rendering,
top-nav "Learn" target, id 404 localization. Also worth folding in as MEDIUM/LOW nav-UI polish: inline
hub-group descriptions, a softer treatment of the "Legacy" label's deprecation connotation, current-
vs-archival visual distinction, breadcrumb Title-Case consistency, the mobile drawer's unexplained
"Drawer width" toggle placement, and the active-nav-item contrast gap (4.37:1 vs 4.5:1 AA).

Out of scope (for now): the URL restructure itself (shipped and passing); the two genuinely in-scope
retest defects (redirect double-hop, breadcrumb 375px wrap) which are fixed inside the restructure
plan's Phase 5, not here; and the apex `ayokoding.com` → `www` forwarding that emits a plaintext-`http`
`Location` and the canonical-domain choice — both are Squarespace domain/registrar configuration, not
application code.

## Risks & open questions

Is the Indonesian locale intentionally frozen (making full three-bucket localization the wrong
investment and a signpost the right one), or is parity actually wanted? Does a translated-slug map for
every route already exist to route the switcher through, or must one be built? Is the sidebar defect
best fixed by ellipsis-truncation, a wider default, or making the existing resize handle discoverable —
and should that fix live in `web-ui` (site-wide) or the app? Do the MEDIUM/LOW nav-UI items belong here
or in the navigation-ui plan (plan-03) already in flight?

## What success looks like + promotion signal

Success: a bilingual visitor can switch locale anywhere under Learn without a 404; no sidebar label is
silently clipped; and the Indonesian locale either has parity or tells the user honestly where the
content is. Promotion signal — ready to become a `backlog/` plan once the id-locale posture question is
answered (localize vs signpost) and the sidebar-fix home (app vs `web-ui`) is decided, since those two
answers determine the plan's size and shape.
