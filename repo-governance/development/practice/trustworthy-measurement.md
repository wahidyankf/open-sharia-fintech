---
title: "Trustworthy Measurement"
description: Before a number is allowed to justify a decision, prove the command produced it, prove it measures the path that actually runs, and prove the metric responds to the thing being changed
category: explanation
subcategory: development
tags:
  - measurement
  - benchmarking
  - false-zero
  - critical-path
created: 2026-08-09
---

# Trustworthy Measurement

A measurement is a claim about the system. Most bad measurements in this repo have not been slightly
wrong — they have been claims about something else entirely, while looking exactly like a good
result. A harness that never ran the command reports a spectacular speedup. A benchmark of an
isolated invocation reports a saving the integrated path never pays. A metric that cannot respond to
the change reports a regression the change did not cause.

None of these are caught by looking harder at the number. Each needs a separate check, before the
number is allowed to justify anything.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)** —
  understand what a measurement actually measured before acting on it.
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)** — a metric moving
  is not a cause; the component on the critical path is.

## The Rules

### 1. Prove the command ran before trusting its timing

A timing harness reports elapsed time whether or not the thing being timed executed. Assert the
**exit code and output** of the measured command, not just its duration.

The failure is silent and reads as success. A `zsh` loop of the form

```bash
for c in "md links validate" "md mermaid validate"; do "$BIN" $c; done
```

does **not** word-split `$c` under `zsh` — the whole string arrives as one argument, every
invocation exits immediately with `unrecognized subcommand`, and the harness reports ~3 ms per
command. That is not a fast run; it is no run at all.

This is the same family as the other builtin-transform traps recorded in this repo — `grep -L`
exiting 0 on files-without-match, `ls` being `eza`-aliased and emitting OSC-8 hyperlinks into
`xargs`, RTK rewriting `git diff` output. In each, a shell builtin quietly transforms the thing
being measured and a false zero reads as a pass.

**Do**: measure under `bash` with an explicit array or a `case`; loop N times and divide; assert
`$?` is 0 and the output is non-empty before recording any duration.

**Do not**: use `python3` (or any interpreter with a ~700 ms cold start) for timestamps around a
sub-second command — the instrumentation swamps the subject.

### 2. Measure the integrated path, not an isolated invocation

A per-invocation benchmark does not predict its saving inside a batched or child-process execution
model. Measure the path that actually runs in production before hard-gating a phase on the number.

Worked example: `prettier` and `markdownlint-cli2` were benchmarked as standalone
`npx --no -- <tool>` invocations (622 ms / 441 ms), yielding a projected ~250 ms per-tool saving and
a `≤ 900 ms` acceptance clause. The real pre-commit path never paid that cost: the registry's
commands were always bare, and the outer batch runner spawns `npx --no -- lint-staged` **once** for
the whole batch, with both tools running as its children on a `node_modules/.bin`-inclusive `PATH`.
The `npx` tax the benchmark measured was never being paid twice. Actual measured saving: −138 ms
(−5.4 %), against a projection of ~500 ms — roughly 4× overstated.

**The tell**: the benchmark and the production path differ in _how the process is spawned_. Whenever
that is true, the isolated number is an upper bound at best.

### 3. Establish the critical path before prescribing a wall-clock remedy

Wall-clock in a fan-out DAG is a **max**, not a sum. It is completely insensitive to everything off
the critical path, so any wall-clock remedy must first prove the component it changes is _on_ it.

Worked example: a CI wall-clock p50 regression (974.5 s → 1,219 s) triggered a pre-authored remedy —
"re-balance group composition." The per-job timeline showed the critical path was the TypeScript
quality gate at 1,033 s, a job the topology change never touched, which had taken 1,030 s and
1,018 s on the same branch _before_ the change. All gate groups finished ~13 minutes clear of the
critical path. Re-balancing them could not have moved wall-clock by one second.

The corollary: **sum-type and max-type metrics do not move together.** Runner-seconds (a sum) fell
47.6 % in the very runs where wall-clock (a max) rose. A plan that treats both as symptoms of one
cause will mis-diagnose whichever it reads second.

### 4. A remedy written before anyone saw a timeline is a hypothesis

Plans routinely pair a metric with a prescribed fix at authoring time. That pairing is a guess about
which component will hold the number. Record it as a guess: when the gate fires, re-derive the
component from the actual timeline before applying the prescribed remedy, and if they disagree, the
timeline wins and the plan's remedy gets corrected in place rather than executed.

## Scope

Applies to any number that will justify a decision: benchmark timings, CI metrics, disk
measurements, coverage figures, and acceptance-clause thresholds in plan gates. It does not apply to
diagnostic prints or exploratory readings that no decision depends on — but the moment one is quoted
in a plan, a gate, or a PR, it is in scope.

## Related Documentation

- [Acceptance clauses must be falsifiable](../workflow/test-driven-development.md) — a target that
  cannot fail is not a target; these rules are how you keep it from failing for the wrong reason.
- [Mechanize Cross-File Invariants](./mechanize-cross-file-invariants.md) — the same instinct
  applied to rules rather than numbers.
- [CI Monitoring](../workflow/ci-monitoring.md) — where CI figures come from and how to read a run.
- [Evidence Capture](../quality/evidence-capture.md) — where a recorded measurement belongs.
