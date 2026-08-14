# Knowledge Capture Phase Scaffolding Fixes (Part 1)

Per the
[Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md):
when silent absence is flagged (no phase, no explicit "none" record anywhere), scaffold the missing
phase and `learnings.md`. Never fabricate learnings execution never actually surfaced — scaffold
structure, not content.

**Confidence**: **HIGH** — the phase is completely absent AND `learnings.md` doesn't exist —
scaffold both. **MEDIUM** — unclear from the plan's history whether execution genuinely surfaced no
learnings — scaffold the phase with the routing rubric and both safety gates intact, but don't
auto-write the explicit "none" escape; flag under `## Manual Review Required`. **FALSE_POSITIVE** — a
phase already exists under different heading wording, or `learnings.md` already carries the explicit
"none" record — don't duplicate; at most rename the heading.

**How to scaffold `learnings.md`** (if absent, at the plan-folder root, sibling to `delivery.md`):

```markdown
<!-- Running log of generalizable learnings surfaced during execution. Triage every entry at
     the Knowledge Capture phase before archival. See
     repo-governance/development/quality/knowledge-capture.md -->
```
