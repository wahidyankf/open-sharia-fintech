# Checker Finding Format and Important Notes

## Finding Format

```markdown
### Finding: [Phase 0 Invariant N / D1 Root File / ...] — [Subject]

**Phase**: [Phase 0 — Parity / Phase 1 — Harness Name]
**Criticality**: [CRITICAL / HIGH / MEDIUM / LOW]
**Confidence**: [HIGH / MEDIUM / FALSE_POSITIVE]

**Current value**:
[Current catalog or filesystem state]

**Expected / Upstream value**:
[Expected value per invariant rule or upstream docs citation]

**Drift description**:
[What changed and why it matters]

**Affected files** (if D6 or Invariants 3–4):
[List of affected files]

**Recommendation**:
[Specific fix — re-sync, update catalog row, update binding files, or human action]
```

## Important Notes

**Progressive Writing**: all findings MUST be written immediately as discovered, never buffered.
**Confidence Propagation**: `[Needs Verification]` → `confidence: MEDIUM`; `[Verified]` →
`confidence: HIGH`. **Conservative Drift Threshold**: flag only substantive changes — a
different filename, a renamed directory, a removed required field, a deprecated config key —
never minor wording differences. **FALSE_POSITIVE Handling**: when a catalog row already
documents the current upstream value accurately, set confidence to FALSE_POSITIVE and log as
`[INFO] No drift detected` — do not count it in the findings total.
