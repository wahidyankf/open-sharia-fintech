# Finding Requirements Hard Rules

Inherited verbatim from the retired `pr-review-maker` monolith. Every finding this agent posts
MUST carry all of the following. A finding missing any element is not ready to post.

1. **Numeric confidence score, 0-100** — how directly the evidence supports the finding.
   **Findings scoring below 80 are hard-dropped and never posted.** This is a hard rule, not a
   suggestion: when in doubt, do not post rather than post a low-confidence guess.
2. **Severity** — exactly one of `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`, per the repo's
   [Criticality Levels Convention](../../../../repo-governance/development/quality/criticality-levels.md).
   See the agent file's own Discipline Charter for this discipline's severity definitions.
3. **Concrete evidence** — the exact `file:line` (or a blob URL + the pinned SHA + line range)
   the finding refers to, and, where the finding cites a repo convention, a link to that specific
   `repo-governance/` rule the change violates. Never a vague "somewhere in this file" reference.
4. **Anti-sycophantic framing** — state what is wrong plainly. Do not soften, hedge, or omit a
   real finding to seem agreeable or to keep the review short. Correctness takes priority over
   pleasantness.
