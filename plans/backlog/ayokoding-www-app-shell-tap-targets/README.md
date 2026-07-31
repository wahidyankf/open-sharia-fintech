# Fix Shared App-Shell Tap Targets Below 24x24 CSS px

> **Status**: Backlog stub (not started). Filed from Rule-15 finding `EWT-005`, surfaced during
> [`ayokoding-www-ai-benchmark-responsive-overhaul`](../../in-progress/ayokoding-www-ai-benchmark-responsive-overhaul/delivery.md)'s
> Phase 11 three-tester retest.

## Context

The Phase 11 exploratory-web-tester finding `EWT-005` measured two shared app-shell tap targets
below the WCAG 2.5.8 24x24 CSS px minimum, reproduced across `en`/`id` at all five breakpoints:

- `apps/ayokoding-www/src/features/app-shell/shell/header.tsx` — the "Learn" (`a[href="/en/browse"]`)
  and "Tools" (`a[href="/en/tools"]`) nav links measured approximately 37.1x20 and 35x20 CSS px at
  1280px.
- `apps/ayokoding-www/src/features/app-shell/shell/footer.tsx` — the "MIT" license link
  (`href="https://github.com/wahidyankf/ose-public/blob/main/LICENSE"`) measured approximately
  24.4x17 CSS px at 390px, both locales.

## Scope

**Out of scope for `ayokoding-www-ai-benchmark-responsive-overhaul`**: this is shared app-shell
chrome rendered on every page of `ayokoding-www`, not `ai-benchmark`-feature code — outside that
plan's `apps/ayokoding-www/src/features/ai-benchmark/` blast radius (confirmed by that plan's own
AC-58 e2e step, which scopes its tap-target check to `[data-testid="ai-bench-page"]`). Deferred here
per that plan's Phase 11 instruction, with the user's standing authorization for out-of-plan-scope
deferrals recorded inline in that plan's `delivery.md`.

**In scope for this future plan**: the header nav links and footer license link above; a decision
on whether the same `TAP_TARGET_MIN_CLASS` (`min-h-6 min-w-6 py-1`) pattern already used across
`ai-benchmark` applies unchanged to app-shell chrome, or needs its own treatment given the shell's
own layout constraints.

## Navigation

Full `brd.md`/`prd.md`/`tech-docs.md`/`delivery.md`/`learnings.md` are not yet authored — this is a
minimal stub recording the finding and its scope until this plan is picked up.
