---
title: "PR-Review Quality Gate — Notes"
description: "Operating notes: strictly-sequential is a hard requirement, seven is a ceiling not a target, AI-attribution posting identity, the eleven live pipeline agents, no extension past the cycle cap, and the sibling-PR staleness pattern."
when_to_use: "Use when clarifying an operating nuance not covered elsewhere — e.g. why sibling-repo PR loops shouldn't run concurrently with the source PR's."
---

# Notes

- **Strictly sequential, never parallel**: this is a hard requirement — the loop's dedup logic and
  the CI-green gate both depend on each cycle observing the previous cycle's fully-settled state.
- **Seven is a ceiling, not a target**: the eligible loop exits at the earliest completed clean cycle
  and never extends past `{input.cycles}` (default 7). The ceiling bounds work; it never waives a
  code-related MEDIUM/HIGH/CRITICAL finding.
- **AI-attribution, not a distinct bot identity**: both agents currently post under the existing
  personal `gh` identity with an explicit AI-attribution footer per comment/reply, because no
  dedicated bot/GitHub App identity is provisioned in this environment. This is a pragmatic fallback,
  not a permanent design decision — revisit if a bot/App identity is provisioned later. This does not
  touch the repo's Git Identity Guardrail (that guardrail governs `git config user.*` for commits;
  this is a `gh`/GitHub-API posting identity, a separate concern).
- **All eleven pipeline agents implemented and wired**: `pr-review-scout-maker`, the nine discipline
  specialists, and `pr-review-synthesis-maker` — defined per the
  [PR Reviewer-Discipline Convention](../../../development/quality/pr-review-disciplines.md) — plus the
  unchanged `pr-review-fixer` are this workflow's live actors as of the `worktree-to-pr-hardening`
  plan's Phase 4 cutover, which retired the single-maker `pr-review-maker` monolith immediately (D2)
  rather than running it alongside the split.
- **No extension past `{input.cycles}`, by design**: a seventh cycle is the last automatic attempt.
  If eligible review reaches it with code-related MEDIUM/HIGH/CRITICAL findings outstanding, the
  [ceiling block](./13-loop-exit-and-block-rules.md#loop-exit-and-block-rules) fires; the PR never merges on the strength of having
  spent more cycles, only on the strength of an actually-empty blocking-findings list.
- **Byte-identity-boundary sibling PRs are a moving target until the source PR converges**: when a
  plan opens a source PR (e.g. `ose-public`) alongside byte-identical mirror PRs in sibling repos
  (e.g. `ose-private`), running all repos' review-cycle loops concurrently from the start
  means every fixer commit on the source PR immediately makes the siblings stale again, and each
  sibling's next cycle re-discovers "stale vs. upstream" as its top finding instead of surfacing new
  issues — a self-correcting but wasteful pattern observed to cost an extra cycle per sibling in
  practice. Prefer running the source PR's loop to completion (CI-green at a stable head) first, then
  starting or resuming each sibling's remaining cycles against that final head — a sibling cycle
  already in flight when the source PR converges can still finish its current pass and resync on its
  own next cycle, but do not deliberately kick off a NEW sibling cycle while the source PR's loop is
  still open.
