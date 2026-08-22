# Finding Requirements and Scope Guard

## Finding Requirements (Hard Rules)

Inherited verbatim from the retired `pr-review-maker` monolith and carried by every specialist.
Every finding this agent includes in the consolidated review MUST carry all of the following — a
finding missing any element does not survive the reasonableness-filter function.

1. **Legible to a junior engineer** — the consequence in plain terms, any cited rule paraphrased
   rather than only linked, and critique aimed at the change rather than its author. See
   [Review as Teaching](../../../../repo-governance/development/quality/pr-review-disciplines/review-as-teaching.md).
1. **Numeric confidence score, 0-100** — how directly the evidence supports the finding.
   **Findings scoring below 80 are hard-dropped and never posted.** This bar applies to the
   consolidated, post-tool-verify score, not merely the specialist's original raw score —
   tool-verify can raise or lower a raw score before this bar is checked.
1. **Refutation clause** — the specialist's stated "what would prove this wrong" carries through to
   the posted finding, revised if tool-verify changed the basis. A surviving finding that names
   nothing checkable is dropped by the reasonableness filter, whatever its score: it gives the fixer
   no independent way to test the claim, and the score alone has been measured not to predict
   acceptance.
1. **Severity** — exactly one of `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`, per the repo's
   [Criticality Levels Convention](../../../../repo-governance/development/quality/criticality-levels.md).
   Re-categorization can change a finding's severity along with its discipline (e.g. a
   re-categorized architecture finding may carry a different severity mapping than the discipline
   that originally raised it).
1. **Concrete evidence** — the exact `file:line` (or a blob URL + the pinned SHA + line range) the
   finding refers to, and, where the finding cites a repo convention, a link to that specific
   `repo-governance/` rule the change violates. Never a vague "somewhere in this file" reference.
1. **Anti-sycophantic framing** — state what is wrong plainly in the consolidated review. Do not
   soften, hedge, or drop a real finding merely to keep the review short; the
   reasonableness-filter drops noise, not substance.

**CRITICAL-requires-reproduction**: a `CRITICAL` finding surviving to the consolidated review must
carry a reproduction/verification step from the tool-verify function, not mere multi-specialist
agreement — unanimous agreement across specialists has been shown to endorse non-existent bugs
absent empirical reproduction.

## Scope Guard

**The loop never widens the PR it reviews.** Scope is the problem the PR body states under
`## Why`, plus the linked plan or issue when one exists. The test for every finding: does fixing
it serve that stated problem, or add a second one? The second is scope creep, however worthwhile
on its own — drop it in the reasonableness filter. This agent never manufactures new scope during
synthesis. **One exception**: a defect this PR itself introduces is always in scope, however far
from the stated problem, or "out of scope" would excuse a regression the PR caused. See
[Scope Guard](../../../../repo-governance/workflows/pr/pr-review-quality-gate/scope-guard-no-scope-creep.md).
