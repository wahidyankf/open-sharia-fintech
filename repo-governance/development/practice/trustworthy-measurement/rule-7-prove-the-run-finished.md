---
description: A run that was killed leaves output that reads exactly like a finished one - record a terminal exit marker as the run's last action and treat its absence as "did not finish", never as "still running" or "passed"
when_to_use: Use whenever a command is backgrounded, wrapped in a timeout, or long enough that its result is read after the fact.
---

# Rule 7: Prove the Run Finished

## 7. A result is complete only when a terminal marker says so

Rule 1 guards against a command that never **started**. This rule guards the other end: a command
that started, produced output, and then died. The two failures look nothing alike in cause and
identical in evidence — a file of plausible output and no error.

A killed run is not rare. A harness timeout sends `SIGTERM` (exit `143`), a supervisor sheds a
child under memory pressure, a wrapper is cancelled between steps. In every case the output written
before the kill survives and reads as the whole result.

**Record the exit code as the run's final action, in the same artifact as its output:**

```bash
mycommand > out.txt 2>&1
echo "TERMINAL_EXIT=$?" >> out.txt
```

Now `out.txt` answers three questions that partial output cannot: did it finish, what did it
return, and is what I am reading all of it.

### Absence of a marker is not absence of a problem

The three readings below are the same observation and only one of them is safe:

| Observation                     | Unsafe reading  | Correct reading                  |
| ------------------------------- | --------------- | -------------------------------- |
| No marker, no process           | "still running" | **did not finish** — investigate |
| No marker, output ends mid-way  | "nearly done"   | **did not finish** — investigate |
| Output says `PASSED`, no marker | "passed"        | **unknown** — no exit code       |

A tool's own prose is not an outcome. `Status: VALIDATION PASSED WITH WARNINGS` printed by a run
that was later killed is a sentence, not an exit code.

### One gated command per unit of background work

Do not chain several gated commands inside one backgrounded wrapper. When the wrapper dies at
command two, command one's success is unattributable and commands three and four never ran — and
the wrapper's own stdout may be empty, so nothing says which. Give each command its own run and its
own marker, so a death strands only itself.

This is also why elapsed time is not evidence: a wrapper that died after ninety seconds and one
still working after ninety seconds are indistinguishable from the outside. Only the marker
distinguishes them.

## Do and Do Not

**Do**: write the marker with `>>` after the redirect, so it survives even when the command itself
writes nothing; check for the marker before reading any result as final.

**Do not**: infer completion from a quiet process table, from elapsed time, from a partially
written file, or from success prose in the output.

## Related Documents

- [Rule 1 — Prove the Command Ran](./rule-1-prove-the-command-ran.md) — the other end of the same
  failure: a command that never started.
- [Resource-Aware Development](../resource-aware-development.md) — admission deferral is a distinct
  outcome from failure and from being killed.
