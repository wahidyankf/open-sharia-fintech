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

## `harness bindings validate` is not registry-driven for agent dirs (Phase 3)

Deleting `harness naming validate` stranded `harness-registry-driven.feature`, whose scenario
claimed two harness commands derive their target sets from `repo-config.yml`. The obvious repair —
repoint the claim at `harness bindings validate` — **failed the test**: against a synthetic repo
whose source tier lives at `.custom-src/agents`, the validator reported
`Failed to read Claude agents directory: .../.claude/agents ... No such file or directory`. It
hard-codes the path.

This does not undo the Phase 3 probe (P3.1), which proved `bindings validate` detects mirror drift
in **this** repository's real layout, in both directions. It does mean the withdrawal lost a
property nothing else carries: no surviving command derives an agent-dir set from the registry, so
adding a twelfth agent-bearing harness now needs a source edit, not just a config edit. The scenario
was narrowed to `harness duplication validate` — the one command the fixture still proves
registry-driven — rather than left asserting something false.

**Routing**: backlog plan. Making `bindings validate` read its agent dirs from the `harness:`
registry is a code change with its own TDD cycle and a cross-repo parity obligation, out of scope
here.

**The general defect**: a spec scenario named two commands and asserted one property of "each". When
one command died, the surviving half of the sentence looked like a safe place to re-point it. It was
not — the property was never true of the replacement. Repointing a spec at a different subject is a
new claim and needs a new test run, not a rename.
