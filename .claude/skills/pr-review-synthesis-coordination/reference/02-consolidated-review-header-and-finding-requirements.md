# Consolidated Review Header and Finding Requirements

## Consolidated Review Header (Every Tier Decision Is Auditable)

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

## Finding Requirements (Hard Rules)

Inherited verbatim from the retired `pr-review-maker` monolith and carried by every specialist.
Every finding this agent includes in the consolidated review MUST carry all of the following — a
finding missing any element does not survive the reasonableness-filter function.

1. **Numeric confidence score, 0-100** — how directly the evidence supports the finding.
   **Findings scoring below 80 are hard-dropped and never posted.** This bar applies to the
   consolidated, post-tool-verify score, not merely the specialist's original raw score —
   tool-verify can raise or lower a raw score before this bar is checked.
2. **Severity** — exactly one of `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`, per the repo's
   [Criticality Levels Convention](../../../../repo-governance/development/quality/criticality-levels.md).
   Re-categorization can change a finding's severity along with its discipline (e.g. a
   re-categorized architecture finding may carry a different severity mapping than the discipline
   that originally raised it).
3. **Concrete evidence** — the exact `file:line` (or a blob URL + the pinned SHA + line range) the
   finding refers to, and, where the finding cites a repo convention, a link to that specific
   `repo-governance/` rule the change violates. Never a vague "somewhere in this file" reference.
4. **Anti-sycophantic framing** — state what is wrong plainly in the consolidated review. Do not
   soften, hedge, or drop a real finding merely to keep the review short; the
   reasonableness-filter drops noise, not substance.

**CRITICAL-requires-reproduction**: a `CRITICAL` finding surviving to the consolidated review must
carry a reproduction/verification step from the tool-verify function, not mere multi-specialist
agreement — unanimous agreement across specialists has been shown to endorse non-existent bugs
absent empirical reproduction.

## Scope Guard

Only include findings that fall within the PR's own declared plan or issue scope in the
consolidated review. This agent does not manufacture new scope-creep asks during synthesis — a
specialist's scope-creep finding is either genuinely in-scope (survives the filter) or is itself
a reasonableness-filter drop.
