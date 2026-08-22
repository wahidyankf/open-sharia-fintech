# A Refutation Clause Must Be Postable

The shape rules govern what the fixer may **run**. They say nothing about whether the clause can be
**posted** — and a clause that cannot be posted fails earlier and more expensively than one that
cannot be run.

This repository enforces its own safety rules through PreToolUse hooks. `guard-env-file-access`
inspects every command an agent is about to execute and blocks any that names a dotfile environment
path. The coordinator posts a review by executing a command whose argument carries the finding text,
so a clause quoting such a path is blocked at the moment of posting: the whole consolidated review
fails, not one finding, and the block consumes whatever tool call was in flight. This happened on
PR #249 cycle 3 — a clause that demonstrated a write to a `.env`-family path took the review down
with it and destroyed the script being written in the same call.

So a clause is written to be read as data by a hook that cannot tell demonstration from intent:

- It never contains a command that **writes**, even as an example of what not to do. Describe the
  unsafe shape in prose and name the rule it breaks; do not spell it out as a runnable line.
- It never names a dotfile environment path, in any position, quoted or not.
- Where a finding is _about_ an unsafe command, the same restraint applies that
  [rule 5](./refutation-clause-execution.md) already places on reporting one: name the shape, never
  reproduce it.

A specialist writing an unpostable clause has written a finding nobody will see. The requirement is
stated on both authoring surfaces for that reason.
