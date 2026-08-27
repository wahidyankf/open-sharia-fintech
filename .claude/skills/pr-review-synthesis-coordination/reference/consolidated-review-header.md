# Consolidated Review Header

Every consolidated review opens with exactly:

```markdown
## PR Review — Single Pass

**Head SHA**: <40-char reviewed SHA>
**Base**: <base ref> at <base SHA>
**Risk tier**: trivial | lite | full
**Probe class**: <class>
**Specialists fanned out**: <selected list or none>
**Per-specialist raw findings**: <counts and named skips>
**Diff coverage**: full diff | N recorded slices
**Prior settled findings respected**: N | none
```

An enclosing cycle may render `## PR Review — Cycle N of M` and add its ordinal, but it must keep
all pass fields. Transcribe routing facts from the scout brief; do not re-derive them. Synthesis
alone populates raw-finding counts. Each posted finding names its originating specialist(s).

The authenticated machine-readable record in
[machine-readable-audit-record.md](./machine-readable-audit-record.md) carries the same pass facts.
