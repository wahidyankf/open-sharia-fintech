# Finding Requirements Hard Rules

Inherited verbatim from the retired `pr-review-maker` monolith. Every finding this agent posts
MUST carry all of the following. A finding missing any element is not ready to post.

1. **Numeric confidence score, 0-100** — how directly the evidence supports the finding.
   **Findings scoring below 80 are hard-dropped and never posted.** This is a hard rule, not a
   suggestion: when in doubt, do not post rather than post a low-confidence guess.
1. **Refutation clause** — one line naming the **specific, checkable evidence that would prove this
   finding wrong**: a command whose output would contradict it, a file whose content would, or an
   observation that would. "I am confident" is not a refutation clause; "if `rg -F 'X' path/` returns
   a hit, this finding is void" is. A finding whose author cannot name what would refute it is a
   suspicion, not a finding, and is not posted. The measured reason this exists: across this repo's
   94 posted findings the confidence score did not predict acceptance (91.5 accepted vs 93.0 not),
   so the score alone leaves the fixer nothing independent to check.
1. **Severity** — exactly one of `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`, per the repo's
   [Criticality Levels Convention](../../../../repo-governance/development/quality/criticality-levels.md).
   See the agent file's own Discipline Charter for this discipline's severity definitions.
1. **Concrete evidence** — the exact `file:line` (or a blob URL + the pinned SHA + line range)
   the finding refers to, and, where the finding cites a repo convention, a link to that specific
   `repo-governance/` rule the change violates. Never a vague "somewhere in this file" reference.
1. **Anti-sycophantic framing** — state what is wrong plainly. Do not soften, hedge, or omit a
   real finding to seem agreeable or to keep the review short. Correctness takes priority over
   pleasantness.
