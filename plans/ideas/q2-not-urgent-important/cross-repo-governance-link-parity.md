# Cross-repo governance link and anchor parity

One-line summary: shared governance docs copied from `ose-public` into a sibling repo carry anchor
links that silently break there, because heading structure is only guaranteed inside the repo the doc
was written in.

> Demoted from a full `backlog/` plan to a two-pager on 2026-08-05. The item was originally captured
> by the Phase 8 Knowledge Capture of the `adopt-cursor-platform-binding` plan (archived 2026-07-28),
> which routed the learning to `plans/backlog/cross-repo-governance-link-parity/`; that folder never
> grew past a three-line stub.

## Problem / context

When a governance document is copied from `ose-public` into a sibling repo, its relative links travel
with it but the **headings they point at do not**. `rhino-cli md links validate` already resolves
`#fragment` references using the GitHub slug algorithm and emits a `broken-anchor` finding when no
matching heading exists — but it only ever sees **one repo at a time**, so a link that is perfectly
valid in `ose-public` becomes a latent break the moment the file lands somewhere else.

This is not hypothetical. During Phase 6 of `adopt-cursor-platform-binding`, `ose-public` governance
was copied verbatim into a sibling repo, and that repo's own pre-push gate blocked on a
`#platform-binding-color-translation` anchor that resolved cleanly in `ose-public` but had no
corresponding heading in the sibling's `ai-agents.md`. The fix was to add a
`### Platform Binding Color Translation` heading in the sibling. The defect was real, but it was
found by the **destination** repo's push gate, mid-landing, rather than by anything the landing
itself ran — so it surfaced as a blocker at the worst moment instead of as a pre-flight check.

The failure mode generalizes past anchors to any relative link whose target path exists in the source
repo and not in the destination: `ose-private` ships a different project set, so
a link into `apps/` or `docs/` that is fine upstream can point at nothing downstream.

## Why now

Multi-repo landings are now routine rather than exceptional, and each one is another chance to
reintroduce the same class of break. The parity boundaries make this worse, not better, because they
cover **different repo sets** and must not be conflated:

- **Content parity** is `ose-public` → `ose-private` only, and it is the boundary along which
  governance prose actually flows.
- **`apps/rhino-cli` byte-identity** spans `ose-public` and `ose-private` — a
  code-shaped boundary that says nothing about doc anchors.
- Governance copies into `ose-private` happen **manually, case by case**; there is no
  classifier-driven content sync between it and `ose-public`, so nothing systematic catches drift
  there at all.

The tooling to detect the break already exists and is already wired into pre-push and the `md-links`
CI gate. What is missing is only the cross-repo application of it — which makes this a cheap win that
gets cheaper the sooner it lands, and more expensive every time a landing eats a blocked push.

## Prior art / precedents

- **Linking Convention § Anchor Links** — specifies the existing `broken-anchor` finding and the
  GitHub slug algorithm (verified against `github-slugger` v2) that any cross-repo check would reuse
  unchanged. [linking.md](../../../repo-governance/conventions/formatting/linking.md)
- **Repository Validation reference** — documents how `md links validate` is wired today: repo-wide
  rather than per-file, running at pre-push and as the `md-links` CI gate job.
  [repository-validation.md](../../../repo-governance/development/quality/repository-validation.md)
- **Multi-repo parity planning workflow** — the propagation fan-out (`ose-public` as source of truth)
  that a pre-flight anchor check would slot into.
  [plan-multi-repo-parity-planning.md](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
- **Related Repositories reference** — the authority on which boundary covers which repos, and the
  reason a naive "check all four" framing is wrong.
  [related-repositories.md](../../../docs/reference/related-repositories.md)
- **adopt-cursor-platform-binding** — the plan whose Phase 6 hit the defect and whose Phase 8 routed
  it here. [README.md](../../done/2026-07-28__adopt-cursor-platform-binding/README.md)

## Proposed direction (sketch)

Reuse the existing validator rather than build a second one. The sketch has three parts:

- **A destination-aware pre-flight check.** Before a multi-repo landing copies a governance file,
  resolve that file's relative links and `#fragment` anchors against the **destination** repo's
  heading and path inventory, not the source's. Report the breaks up front so the landing can carry
  the accompanying heading fix in the same change.
- **A shared-surface scope.** Restrict the check to the governance documents that actually flow
  across the content-parity boundary, rather than sweeping every markdown file in both trees.
- **Findings that name the fix.** Emit the missing heading text (or missing path) per finding, so the
  remedy is "add this heading in the sibling" rather than "go re-derive what upstream meant".

## Rough scope & non-goals

In scope:

- Detecting broken relative links and broken anchors introduced by copying a shared governance doc
  across the content-parity boundary.
- Reusing the existing slug algorithm and `broken-anchor` finding shape, so upstream and cross-repo
  results are directly comparable.

Out of scope (for now):

- **Auto-repairing** the sibling — inserting or renaming headings automatically; the check detects,
  a human or a plan step fixes.
- **External (`http`) link checking** — that is a separate concern with separate caching and failure
  modes.
- **Any change to the slug algorithm or the `broken-anchor` finding definition** themselves.
- **The `apps/rhino-cli` byte-identity boundary** — a different boundary over a different repo set,
  already tracked as its own idea.
- **`beaver-nest`**, which sits outside the parity loop entirely.

## Risks & open questions

- **Where does the check run?** A cross-repo check needs both trees present. Does it run in the
  landing worktree (which already has the source), in the destination's CI, or as an explicit step in
  the parity workflow? (open)
- **How does it read the destination repo**, given `ose-private` may be a bare repo and
  is private with no public read access? (open)
- **Which files count as "shared governance surface"?** An explicit registry is more predictable but
  needs maintenance; deriving the set from what a landing actually copies is self-maintaining but
  only knows the answer mid-landing. (open)
- **Divergence is sometimes correct.** Siblings legitimately differ — `ose-private` ships a
  different project set than `ose-public` — so a strict "anchors must match"
  rule would produce false positives. The check needs a way to record intentional divergence. (open)
- Rabbit hole: this could grow into a general cross-repo doc-diff engine. It should stay a link and
  anchor resolution check.

## What success looks like + promotion signal

Success: a multi-repo governance landing never gets blocked by a broken anchor at the destination's
push gate, because the break was reported before the copy and fixed in the same change. The
`broken-anchor` finding stays the single vocabulary for the defect, whichever repo surfaces it.

Promotion signal: promote to a full `backlog/` plan when **either** (a) a second multi-repo landing
is blocked by a broken link or anchor in a sibling — proving this is a recurring class rather than a
one-off — **or** (b) the run-location and destination-read questions above are answered concretely
enough to design against, most likely as a by-product of whatever mechanism the `apps/rhino-cli`
byte-identity gate settles on for cross-repo access. Until one of those lands, the honest state is
"one confirmed occurrence, mechanism unresolved" — not ripe.
