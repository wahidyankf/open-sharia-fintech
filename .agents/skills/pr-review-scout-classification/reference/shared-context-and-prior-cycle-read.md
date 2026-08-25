# Shared-Context Assembly, Once (D13)

Assemble a single shared-context brief — the **pinned head SHA** from Core Responsibility step 1,
PR metadata (title, body, author), the linked plan/issue context, and the **full diff** — **once
per cycle**, and hand the identical brief to every specialist selected for this cycle's route, and
to `pr-review-synthesis-maker`, rather than each downstream consumer separately re-deriving the
same context (which would otherwise multiply token cost by the number of specialists fanned out).

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

Before choosing the ordinal or fanning out, rehydrate every cycle review, v3 disposition (legacy
v2 means `dismisses-finding`), cycle non-credit event, probe, checkpoint, clean result, and used
ceiling. Stop on malformed, duplicate, or conflicting history; never reset to cycle 1 or empty
`prior`.

Then read the **prior cycle's thread resolution status** via the Reviews API, including any thread a **human explicitly
dismissed** ("won't fix" / "I disagree"). A human dismissal **resolves** that thread going
forward, mirroring a fixer rejection whose effect is `dismisses-finding`. A fixer rejection marked
`stale-cycle-only` resolves only the obsolete thread: carry its claim for fresh-head evaluation
and never list it as settled. Record this
resolution state in the shared-context brief and feed it to the specialists (alongside the rest
of the brief) so no specialist wastes a finding re-litigating something a human has already
settled, and so `pr-review-synthesis-maker` never re-surfaces a dismissed finding in the
consolidated review it posts.

## Review-Route Read-Back

Before fan-out, read the PR body and verify its review-route record names the pinned base/head,
frozen outcome/scope, classification evidence, risk, selected and skipped lenses with reasons,
current checks, settled threads, and this cycle's changed probe. Treat a missing or stale record as
a routing defect to correct before specialist review; it is human-readable audit evidence, not a
new enforcement mechanism.
