# Propagate the `APP_ENV` tiered-env-file convention to `ose-primer`

One-line summary: port `restrict-env-access-to-prod-and-stag`'s `APP_ENV` tier convention (guard
rewrite, `.gitignore` entries, `rhino-cli env init`/`env_staged_guard` changes, and the per-language
env-loader pattern) from `ose-public`/`ose-private` to `ose-primer`, which has not received any of it.

> Idea, added 2026-08-13 — captured from `restrict-env-access-to-prod-and-stag`'s Phase 10
> Knowledge Capture (`plans/done/2026-08-13__restrict-env-access-to-prod-and-stag/learnings.md`).
> Relocated from ose-private/plans/ideas/propagate-env-tier-to-ose-primer.md on 2026-08-19 by plan-ideas-grooming.

## Problem / context

`restrict-env-access-to-prod-and-stag` (delivered in `ose-public` PR #176 and directly to
`ose-private` main) rewrote how every app in scope handles `.env.prod`/`.env.stag`: a hardened
`block-env-file-access.sh` guard, a narrowed `.claude/settings.json` deny-list, `.gitignore` entries
for both restricted tiers, `rhino-cli env init`/`env staged-guard` changes, and a shared
`APP_ENV`-driven tier loader (`libs/ts-env-loader`, `libs/fsharp-env-loader`) consumed by every
Next.js app and F# backend. None of this reached `ose-primer` — its `.gitignore`, `.claude/hooks/`,
`apps/rhino-cli`, and app-level env loaders are still on the pre-plan shape, per this plan's own
`README.md §Out of scope` and `tech-docs.md` DD-8 (`ose-primer` explicitly deferred under the
delayed-sync principle).

## Why now

Not urgent by itself — `ose-primer` is a downstream template repo with its own cadence, and nothing
today depends on it carrying this convention. It becomes blocking the moment any future plan or
session touches `ose-primer`'s `.gitignore`, `.claude/hooks/`, `apps/rhino-cli`, or
`repo-governance/` — at that point the drift must be resolved as part of that work, not deferred
again. **This is the explicit bounded trigger**, not an open-ended "someday."

## Prior art / precedents

- **`restrict-env-access-to-prod-and-stag`** (this idea's source plan) —
  [`plans/done/2026-08-13__restrict-env-access-to-prod-and-stag/`](https://github.com/wahidyankf/ose-private/blob/main/plans/done/2026-08-13__restrict-env-access-to-prod-and-stag/README.md)
  is the complete reference implementation to port.
- **Related Repositories §Sync cadence across repos** —
  [`docs/reference/related-repositories.md`](../../../docs/reference/related-repositories.md) — the
  delayed-sync principle this idea operates under, and the source of the "explicit bound, not
  unbounded deferral" requirement above.
- **`ose-public` ↔ `ose-primer` content-parity workflow** — the existing mechanism this idea would
  reuse to carry the convention across, rather than inventing a new sync path.

## Proposed direction (sketch)

- Diff `ose-primer`'s current `.gitignore`, `.claude/hooks/`, `.claude/settings.json`,
  `apps/rhino-cli`, and each app's env-loading code against `ose-public`'s post-plan state.
- Port the guard script, deny-list, `.gitignore` entries, and `rhino-cli` verbs first (the
  enforcement layer), then the per-app loader migrations.
- Reuse `libs/ts-env-loader`/`libs/fsharp-env-loader` if `ose-primer`'s app set overlaps; otherwise
  scope a primer-appropriate equivalent.

## Rough scope & non-goals

In scope: `ose-primer`'s `.gitignore`, `.claude/hooks/block-env-file-access.sh`,
`.claude/settings.json` deny-list, `apps/rhino-cli` env commands, and app-level `APP_ENV` loaders.

Out of scope: any change to `ose-public`/`ose-private` (already done); inventing a new convention —
this is a port, not a redesign.

## Risks & open questions

- Does `ose-primer`'s app set match `ose-public`'s closely enough to reuse the shared libs directly,
  or does it need its own polyglot-loader sweep (the scope this plan explicitly cut per DD-8)? (open)
- Has `ose-primer` diverged further since 2026-08-13 in ways that make a straight port riskier? (open)

## What success looks like + promotion signal

Success: `ose-primer` enforces the same `.env.prod`/`.env.stag` restriction and `APP_ENV` tier
convention as `ose-public`, verified by the same class of hash/diff checks this plan ran in its own
Phase 9. Promote to a full `backlog/` plan the moment the bounded trigger fires — the next plan or
session touching any of `ose-primer`'s `.gitignore`, `.claude/hooks/`, `apps/rhino-cli`, or
`repo-governance/` surfaces.
