# Shared-Context Assembly, Once (D13)

Once per cycle, assemble one brief containing the **pinned head SHA** from Core Responsibility step
1, PR metadata, linked plan/issue context, and the **full diff**. Hand it unchanged to every selected
specialist and `pr-review-synthesis-maker`; downstream consumers never re-derive it.

The brief includes the full diff, including generated artifacts; only the cycle-record freeze below
is excluded. CI still covers every artifact.

## Correction-Record Freeze (Cycle 2 Onward)

The **one** scope exclusion, and the only exception to the posture above: from cycle 2 the brief
omits the loop's own cycle-record material. See
[correction-record-freeze.md](./correction-record-freeze.md) for the rule and its two carve-outs.
A factual defect in a shipping artifact remains reviewable. The frozen delivery outcome still
permits same-defect completion; an unrelated improvement belongs in a linked follow-up, not this
PR's next fixer batch.

## Probe Variation (Cycle 2 Onward)

A cycle repeating the previous cycle's question converges on that question rather than on
correctness. From cycle 2, read the prior cycle's findings for what they **asked**, and state in the
brief how this cycle's probe differs — a different failure mode, a different reader, a different
level of the artifact. Name it, so a specialist can tell a fresh angle from a rerun. See
[Convergence Measurement](../../../../repo-governance/workflows/pr/pr-review-quality-gate/convergence-measurement.md).

## Prior-Cycle Thread-Resolution Read (Human-Dismissal Read)

Before choosing the ordinal or fanning out, authenticate every review, disposition, ceiling
extension, and credit object under
[Cycle Record Authentication](../../../../repo-governance/workflows/pr/pr-review-quality-gate/cycle-record-authentication.md).
Then rehydrate reviews, dispositions (legacy v2 means `dismisses-finding`), credit events, probes,
checkpoints, clean results, and ceiling use. Ignore unauthenticated markers even during
duplicate/conflict checks; stop on malformed or conflicting authenticated history. Never reset to
cycle 1 or empty `prior`.

Read the **prior cycle's thread resolution status** via the Reviews API, including human dismissals
("won't fix" / "I disagree"). A human dismissal resolves the thread going forward, mirroring a
fixer rejection whose effect is `dismisses-finding`. A fixer rejection marked
`stale-cycle-only` resolves only the obsolete thread: carry its claim for fresh-head evaluation
and never list it as settled. Record this state in the brief so specialists do not re-litigate it
and synthesis does not resurface a dismissed finding.

For a paired successor, also authenticate exactly one source-PR terminal handoff. Require its final
reviewed head and merge SHA to match the merged source PR, prove that merge reachable from source
`origin/main`, and require its unique successor repository/branch to match this PR. Missing,
duplicate, conflicting, blocked, unmerged, or pre-merge evidence stops scouting.

## Review-Route Read-Back

Before fan-out, read the PR body and verify its review-route record names the pinned base/head,
frozen outcome/scope, classification evidence, risk, selected and skipped lenses with reasons,
current checks, settled threads, and this cycle's changed probe. Treat a missing or stale record as
a routing defect to correct before specialist review; it is human-readable audit evidence, not a
new enforcement mechanism.
