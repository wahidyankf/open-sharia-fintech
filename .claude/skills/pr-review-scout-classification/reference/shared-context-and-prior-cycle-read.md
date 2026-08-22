# Shared-Context Assembly, Once (D13)

Assemble a single shared-context brief — the **pinned head SHA** from Core Responsibility step 1,
PR metadata (title, body, author), the linked plan/issue context, and the **full diff** — **once
per cycle**, and hand the identical brief to every specialist selected for this cycle's tier, and
to `pr-review-synthesis-maker`, rather than each downstream consumer separately re-deriving the
same context (which would otherwise multiply token cost by the number of specialists fanned out).

## No-Exclusion Posture (Full Diff, No Generated-File Filtering)

One exception applies from cycle 2 — see the correction-record freeze below.

This brief carries the **full diff with NO generated-file exclusion** — reviewers see everything,
including `.opencode/agents/**`, `.codex/agents/**`, `.agents/skills/**`, `generated/**` (e.g. `search-data.json`),
`package-lock.json` and other lock files, minified assets, source maps, and any file carrying an
`@generated` / "DO NOT EDIT" marker. Nothing is silently filtered out before a specialist reviews
it — the rationale is explicitness: a hand-edited "generated" file is never silently missed
because nothing is silently excluded. CI still runs over everything regardless of what any
reviewer chooses to skim.

## Correction-Record Freeze (Cycle 2 Onward)

The **one** scope exclusion, and the only exception to the posture above: from cycle 2 the brief
omits `plans/**`. See
[correction-record-freeze.md](./correction-record-freeze.md) for the rule and its two carve-outs.

## Large-Diff Posture (Scout's Discretion)

For a `full`-tier PR whose unfiltered diff exceeds a specialist's comfortable context budget, you
**MAY** have specialists review per-domain-relevant file slices rather than the whole diff at
once — record this slicing choice in the shared-context brief so `pr-review-synthesis-maker`
carries it into the review header it posts. If a diff still cannot be reviewed in one fan-out,
record an explicit "diff exceeds single-review scope — reviewed in N slices" note in the brief
rather than silently under-covering it.

## Probe Variation (Cycle 2 Onward)

A cycle repeating the previous cycle's question converges on that question rather than on
correctness. From cycle 2, read the prior cycle's findings for what they **asked**, and state in the
brief how this cycle's probe differs — a different failure mode, a different reader, a different
level of the artifact. Name it, so a specialist can tell a fresh angle from a rerun. See
[Convergence Measurement](../../../../repo-governance/workflows/pr/pr-review-quality-gate/convergence-measurement.md).

## Prior-Cycle Thread-Resolution Read (Human-Dismissal Read)

Before fanning out a new cycle, read the **prior cycle's thread resolution status** on the PR —
via `gh api` against the PR's review threads/comments — including any thread a **human explicitly
dismissed** ("won't fix" / "I disagree"). A human dismissal **resolves** that thread going
forward, mirroring `pr-review-fixer`'s own reasoned-reject on the agent side. Record this
resolution state in the shared-context brief and feed it to the specialists (alongside the rest
of the brief) so no specialist wastes a finding re-litigating something a human has already
settled, and so `pr-review-synthesis-maker` never re-surfaces a dismissed finding in the
consolidated review it posts.
