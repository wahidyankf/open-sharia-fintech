# Rule 15: Phase-Gate and Natural-Pause Validation (Step 5i — MANDATORY HARD RULE)

Enforces
[Plans Convention §Phased Delivery: Natural Pauses and Phase Gates](../../../../repo-governance/conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule):
every phase ends at a natural pause and closes with an explicit gate.

**What to validate**:

1. **Every phase has a `### Phase N Gate`** — including Phase 0 and the final verification phase.
   Missing: **HIGH** per phase.
2. **Gate has both required parts** — (a) a must-pass verification checklist opening with "all checks
   must pass before starting Phase N+1", executor-tagged with explicit commands and expected results,
   and (b) a `**Pause Safety**` blockquote stating the safe-to-stop state and the resume command.
   Missing either: **MEDIUM**.
3. **Each phase is a natural pause** — after the phase, the repo reaches a self-consistent,
   safe-to-stop state (clean tree or intentional no-op; no half-applied migration, broken build,
   staged secret, or resource left mid-mutation). Unsafe stop-state: **MEDIUM** — remedy: merge with
   an adjacent phase rather than weaken the gate.
4. **No invented pauses** — two adjacent phases each claiming a pause that isn't actually safe: flag
   the split **MEDIUM**, recommend merging.

**Grandfathering — in-progress plans predating the convention**: per
[Plans Organization Convention §Applicability](../../../../repo-governance/conventions/structure/plans/phases-as-natural-pauses.md#phases-as-natural-pauses-with-clear-gates-hard-rule),
the Execution-Marker and Phase-Gate HARD RULES apply to net-new plans at authoring time. Plans already
under `plans/in-progress/` when the convention landed are grandfathered — do not raise HIGH findings
against them solely for missing `[AI]`/`[HUMAN]` markers or missing gate/Pause-Safety notes; flag
those omissions only on phases newly added or edited. A net-new plan gets no grace. Note grandfathered
skips as below-threshold informational items, not HIGH findings.

**Finding severity**: phase missing its Gate: **HIGH** per phase. Gate missing the checklist or Pause
Safety note: **MEDIUM** per phase. Non-genuine-pause phase (should merge): **MEDIUM** per phase.
