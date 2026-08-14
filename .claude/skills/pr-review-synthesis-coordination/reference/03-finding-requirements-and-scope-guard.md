# Finding Requirements and Scope Guard

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
