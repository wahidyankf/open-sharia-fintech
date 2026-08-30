# Rule 18: Knowledge Capture Phase Presence (Step 5l — MANDATORY)

Enforces the
[Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md):
every substantive plan's `delivery.md` carries a final Knowledge Capture phase triaging the transient
`learnings.md` log — through the open-ended principle-based triage rubric, the code-routing rule, and
both safety gates — before archival.

**What to validate**:

1. **Phase presence** — a phase referencing triaging `learnings.md` against the routing matrix and
   both safety gates, positioned as the FINAL substantive phase, immediately before Plan Archival.
2. **Explicit "none" record PASSES** — a `No generalizable learnings — <reason>` escape is a PASS, not
   a finding; only silence is penalized.
3. **Silent absence is the only violation** — no phase AND no explicit "none" record anywhere:
   **MEDIUM**, per
   [Criticality Levels Convention](../../../../repo-governance/development/quality/criticality-levels.md).
4. **Code-routing rule stated** — the phase states a learning routed to `apps/`/`libs/`/tests is
   never landed inline (current-plan-blocker carve-out aside); it becomes a separate
   `plans/ideas/` two-pager only with literal authorization and never a directly created backlog
   folder, otherwise `Reported without plan authorization` with handoff evidence. Missing:
   **MEDIUM**.
5. **Both safety gates present** — references applying the secret/sensitivity gate and the
   repo-relevance gate to every surviving entry. Missing either: **MEDIUM**.
6. **`plans/ideas/` overlap-scan rule stated** — if the routing matrix names `plans/ideas/` (default),
   the phase states any entry routed there is checked against `plans/ideas/README.md` and existing
   two-pagers first, folding in rather than duplicating, per
   [Integrate Before You Add](../../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers).
   Silent: **MEDIUM**.
7. **Exemption** — pure-docs/trivial plans may skip an elaborate phase; the explicit "none" escape
   satisfies it. Illegitimate exemption on a substantive plan: **MEDIUM**.

**Finding severity**: no phase and no "none" record: **MEDIUM**. Explicit "none" record present: PASS
(not a finding). Phase present but missing the code-routing rule, either safety-gate reference, or
the `plans/ideas/` overlap-scan rule: **MEDIUM**. Illegitimate trivial-plan exemption: **MEDIUM**.
