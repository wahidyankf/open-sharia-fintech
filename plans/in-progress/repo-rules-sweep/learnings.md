# 🧠 Learnings — Repo Rules Sweep

> Running log. Append in the moment; never reconstruct afterwards. Drained by the Phase 6 Knowledge
> Capture phase before archival. Never the system of record.

## Entries

- _(none yet — execution has not started)_

## Execution finding: `governance-readme-index` crashes intermittently in pre-push

Observed twice during Phases 0 and 1 (2026-08-18). `git push` failed with
`Error: gate governance-readme-index failed`, once accompanied by a Rust panic
(`run with RUST_BACKTRACE=1`). Both times the identical gate passed when re-run
standalone (`rhino gate run --surface=pre-push` → exit 0) and the push succeeded
on retry with no code change in between.

Why it matters: the gate's 439 findings are all `unannotated`, which is NOT in its
declared `fail-kinds` (`missing`, `orphan`, `ghost`), so it should never fail. A
non-deterministic crash in a pre-push gate is indistinguishable from a real
governance violation at the moment it fires, and the same gate runs in CI — where a
retry is far more expensive.

Do not diagnose this from the banner text: the command prints
`README INDEX AUDIT FAILED: 439 finding(s)` even when it exits 0, so the banner is
not evidence of failure. Assert the exit code.

Routing: file as a `plans/backlog/` item against `rhino-cli` — reproduce under
concurrent invocation, then fix the panic path.

## A wrapped inline code span defeats the vendor audit's backtick pairing

`repo-governance vendor validate` strips inline code spans per line (`strip_non_prose` →
`inline_code_re`). When a code span straddles a line wrap, the pairing on the following line starts
from the span's closing backtick and mis-pairs from there, so a later genuinely-fenced term is left
looking like bare prose.

Concretely, reflowing a paragraph to

```text
... sit outside both gates: `harness bindings
generate` emits them from `.claude/`, so any index ...
```

made the audit report `.claude/` → `"primary binding directory"` on a line that contains no
`.claude/` at all. Keeping `` `harness bindings generate` `` on one line cleared it with no wording
change.

**Rule of thumb**: never let an inline code span cross a line break in `repo-governance/` prose.
Prettier will not do this to you — it only happens when a human or agent hand-wraps.

**Follow-up (not this plan's scope)**: the audit should pair backticks over the whole document, or
at least track an open-span carry across lines, instead of resetting per line. Filed for a backlog
plan; the plan in hand is about filename ordinals, not the vendor scanner.
