# Consolidated Review Header (Every Tier Decision Is Auditable)

## Fixed-Shape Header Fields

Every consolidated review this agent posts opens with a fixed-shape header, so the cycle number,
the risk-tier decision `pr-review-scout-maker` made this cycle, which specialists actually fired
(and their raw yield), and any diff-slicing choice are auditable directly from the GitHub review
itself — not just from an internal log:

```markdown
**Cycle**: N of {total}
**Risk tier**: trivial | lite | full
**Specialists fanned out**: none (coordinator-only pass) | governance, logic, security, integrity | all nine specialists (minus any DD-10 content-type skips, named with reason)
**Per-specialist raw findings**: architecture 1, logic 1, governance 2, security 1, integrity 0 (skipped: no test/CI files in diff), performance 1, docs 6, instruction 3, types 0 (skipped: no typed source in diff)
**Security-sensitive-path override applied**: yes | no
**Diff coverage**: full diff reviewed in one pass | reviewed in N slices (see note)
**Prior-cycle human dismissals respected**: N threads / none this cycle
```

Populate every field for every cycle, even a `trivial`-tier coordinator-only pass — an empty or
omitted field is itself a finding-worthy gap in this agent's own output. Every field after
`**Cycle**` carries forward the exact tier, specialist-set, and slicing decision
`pr-review-scout-maker` recorded in its shared-context brief for this cycle — this agent
transcribes that decision into the header, it does not re-derive it. **`**Per-specialist raw
findings**` is the one field this agent itself populates** (not scout) — it is a direct byproduct
of running the Four Coordination Functions over the specialists' actual raw output this cycle, so
it belongs to this agent's own accounting, not scout's pre-fan-out brief.

Every posted finding in the review body also carries a **`**Raised by**:`** line naming the
originating specialist(s) — single name for a single-specialist finding, every contributing name
(comma-separated) for a Deduplicate-function merge — immediately after that finding's
confidence/severity line, so a reader (or a future automated pass over this repo's PR history)
can reconstruct per-specialist acceptance rate directly from the posted review body without
needing a side log.
