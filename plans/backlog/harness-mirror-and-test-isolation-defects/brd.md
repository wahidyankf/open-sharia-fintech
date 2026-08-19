# Business Requirements — Harness Mirror and Test-Isolation Defects

## The problem in one line

Three trees are being treated as uniform when they are not, and in each case the tool reports success
while doing something the maintainer did not intend.

## What was observed

| Defect | Observation                                                                             | Evidence                                       |
| ------ | --------------------------------------------------------------------------------------- | ---------------------------------------------- |
| WS-H1  | `opencode agent list` returns an agent literally named `README`                         | that plan's `evidence/opencode-agent-list.txt` |
| WS-H2  | Adding two `run(...)` smoke tests made an unrelated sibling test fail under parallelism | `update-harness-support` Phase 5 notes         |
| WS-H3  | 47 anchors across 22 skill files resolve to nothing; repo-wide broken-link count is 312 | `update-harness-support` Phase 6 notes         |

## Cost of doing nothing

**WS-H1 — the repository ships noise into someone else's tool.** Every OpenCode user who opens the
agent picker in this repository sees an entry that does nothing. The cost is small per user and
permanent, and it grows with each harness that globs a directory the emitter also writes an index
into. It is also a correctness signal: an agent roster that contains a non-agent means the count
this repository publishes about itself is wrong by one.

**WS-H2 — the suite currently decides what may be tested.** A test that cannot be added without
making a sibling flake is a cap on coverage, and the cap is invisible: it shows up as an unrelated
red run, which invites the wrong fix (re-run it, mark it flaky, reduce parallelism). The two tests
that would have covered the generate path were dropped, so that path is thinner than the checklist
implies.

**WS-H3 — 47 broken references sat unmeasured for as long as the exemption existed.** Skills are
instructions loaded into an agent's context; an anchor pointing at a heading that no longer exists
sends a reader — human or agent — to the wrong place. The exemption was written to stop the
validator from complaining about a tree; it also stopped anyone from learning the tree was wrong.

## Success criteria

1. `opencode agent list` at the repository root returns only real agents, and a gate fails if a
   non-agent file is emitted into a globbed binding directory.
2. Every test in `apps/rhino-cli` passes under the default parallel runner, repeatedly, with no test
   depending on the process working directory.
3. The 47 dangling anchors are zero, measured by the link validator with the skill-tree exemption
   temporarily lifted, and the repo-wide broken count is no worse than the 312 baseline.

## Non-goals

Changing the supported harness set. Redesigning the binding emitters. Removing the skill-tree link
exemption permanently — narrowing it to prove the repair is a step in the work, not the outcome.
