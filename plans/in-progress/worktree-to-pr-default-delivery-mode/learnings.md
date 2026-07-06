# Learnings — Worktree-to-PR Default Delivery Mode

> Running log per the Knowledge Capture convention. All entries below (Phases 0–5) are triaged.

---

## Learning: newly-authored `.claude/agents/*.md` files are not invocable by `subagent_type` within the same session that created them

- **Context**: Phase 3 created `pr-review-maker.md` and `pr-review-fixer.md` as new agent definition
  files. Phase 4's PR-Review Maker→Fixer Cycle (against ose-primer PR #3) needed to invoke both agents
  by name, in the same continuous session.
- **Observation**: neither `pr-review-maker` nor `pr-review-fixer` appeared in the Agent tool's
  available `subagent_type` list, even though the files existed on disk and were correctly formed —
  the available-agent-types list appears to be a snapshot taken at session/process start, not a live
  directory read. Workaround used: invoke `general-purpose` and instruct it, as its first step, to
  `Read` the specific agent `.md` file in full and follow its instructions verbatim, then perform the
  task. This produced equivalent behavior (same tool restrictions honored by convention, same
  procedure followed) without requiring the actual `subagent_type` registration.
- **Why it might generalize**: any future plan that authors a new agent and then needs to invoke it
  within the same plan-execution run (not a rare pattern — `plan-execution.md` Step 8 exists
  specifically to wire freshly-created agents into a review loop) will hit this exact gap. Undocumented,
  a future executor could wrongly conclude the new agent is broken rather than simply unregistered
  this session.
- **Litmus**: PASSES — documenting the workaround (Read-and-follow-verbatim via `general-purpose`)
  gives every future same-session agent-then-invoke plan a known, working path instead of rediscovering
  it.
- **Secret/sensitivity gate**: no secrets involved — pure harness/tooling behavior.
- **Repo-relevance gate**: applies to all three repos equally (harness-level behavior, not
  repo-specific content) — safe to route as a shared governance note.
- **Routing decision**: **routed** to `repo-governance/development/agents/ai-agents.md` §Creating New
  Agents §Testing — added a "Same-session invocation gap" note with the `general-purpose` +
  Read-and-follow-verbatim workaround.

---

## Learning: a background agent dispatched to run a very long multi-step sequence (provision → PR → edits → gates → push → CI-monitor → review-cycle → flip-ready) ended its turn mid-sequence and needed an explicit resume

- **Context**: Phase 5's ose-infra port was dispatched as a single background-agent invocation covering
  ~10 sequential steps, including an open-ended CI-monitoring poll loop.
- **Observation**: the agent's task-notification reported `status: completed` with a result of "CI
  monitor armed, polling every 2 minutes. Waiting for it to report all checks terminal before
  proceeding" — i.e., it stopped before finishing, mid-poll-loop, rather than either finishing the
  whole sequence or explicitly reporting a blocker. It required a `SendMessage` resume (with the full
  remaining steps restated) to continue toward completion.
- **Why it might generalize**: any future orchestration that hands a single background agent an
  open-ended polling loop nested inside a longer multi-step sequence risks the same silent mid-loop
  stop. A future orchestrator that doesn't expect this (e.g., assumes single-shot completion and
  moves on without checking the actual reported state) could wrongly treat "completed" as "finished
  the whole task."
- **Litmus**: PASSES — a documented pattern ("don't delegate an open-ended CI-poll loop as a buried
  step inside a long background-agent sequence; either let the main thread own CI polling via
  `ScheduleWakeup`, or expect and plan for a resume") would let a future executor avoid
  misinterpreting a mid-sequence stop as true completion.
- **Secret/sensitivity gate**: no secrets involved.
- **Repo-relevance gate**: shared across all three repos (agent-orchestration behavior, not
  repo-specific).
- **Routing decision**: **routed** to `repo-governance/development/agents/subagent-orchestration.md` —
  added a new "Delegating an Open-Ended Poll Loop Inside a Long Chunk" anti-pattern entry after
  "Monolithic Chunks Assigned to Single Agents".

---

## Learning: PR-review cycle's "final cycle must be thorough, not a rubber-stamp" instruction worked as intended

- **Context**: Cycles 1 and 2 of the ose-primer PR #3 review found zero ≥80-confidence findings.
  Cycle 3 (final) was explicitly instructed to review genuinely rather than assume cleanliness, and
  found one real (LOW-severity) link-label mismatch that cycles 1–2 missed.
- **Observation**: the workflow behaved exactly as designed — confirms, rather than reveals a gap in,
  the existing `pr-review-quality-gate.md` design.
- **Litmus**: FAILS — nothing durable to change; this validates an existing mechanism.
- **Routing decision**: **discarded** — reason: confirms existing, already-documented workflow
  behavior; not a new generalizable fact.

---

## Learning: link text can legitimately mismatch its (mechanically valid) anchor target — a distinct bug class from the anchor-breakage-from-heading-rename class already fixed 3×

- **Context**: the Cycle 3 finding was a link whose text read "Delivery Mode" but whose anchor
  correctly resolved to a different, same-file heading ("The `worktree-to-pr` Terminal Step") — the
  anchor itself was not broken, only the label was misleading.
- **Observation**: this is a semantic-judgment defect (does the label describe what it points to?),
  distinct from the mechanical anchor-resolution defects the repo's existing `links`/`heading-hierarchy`
  validators already catch. It is not obviously automatable (requires understanding intended meaning,
  not just slug matching).
- **Litmus**: borderline — no clear automatable check to add; forcing a backlog item here would be
  speculative tooling work with an unclear payoff.
- **Routing decision**: **discarded** — reason: caught this time by a careful maker review pass (the
  mechanism that exists to catch exactly this kind of judgment call); no concrete automatable rule to
  add without over-engineering a semantic-similarity linter for uncertain benefit.

---

## Learning: a single green-CI reading is not sufficient proof a background agent's own poll loop has silently stopped

- **Context**: Phase 5's ose-infra port hit the same mid-poll-loop stop as the earlier learning above
  (background agent `aa0cc284970d15ffd` armed a CI-wait then went `completed` before flipping the PR
  to ready). The main thread then took over CI monitoring directly via repeating `ScheduleWakeup`
  cycles (~270s apart) rather than resuming the agent blindly. Across roughly 8 poll cycles, CI
  progressed steadily (5 → 8 → 10 → 11 → 12 → 13 → 15 → 17 → 19 passing checks) before finally
  reaching fully green — at no point during that climb was it actually safe to conclude the agent had
  stalled, because CI was still visibly moving.
- **Observation**: once CI did reach fully green for the first time, escalating immediately (assuming
  the agent's own wait had also seen green and simply failed to act) would have raced the agent's own
  next poll tick — a plausible source of duplicate or conflicting action (e.g., two callers both
  invoking `gh pr ready`). Requiring a **second consecutive** green reading, with the PR's review
  count and `headRefOid` also unchanged across both readings, gave a clean, low-risk signal that
  nothing was moving — at which point the main thread ran the single mechanical `gh pr ready` command
  itself.
- **Why it might generalize**: any future hand-off of an open-ended CI-wait to a background agent
  (the pattern already flagged as an anti-pattern above) will face the identical judgment call about
  when to conclude the agent silently stopped versus is still legitimately mid-cycle. A concrete
  debounce rule (2 consecutive green + no state movement) is directly reusable, not specific to this
  plan.
- **Litmus**: PASSES — a concrete, checkable debounce rule prevents both false-positive escalation
  (racing a live agent) and false-negative under-escalation (waiting forever on a truly-dead agent).
- **Secret/sensitivity gate**: no secrets involved — pure orchestration/monitoring behavior.
- **Repo-relevance gate**: shared across all three repos (agent-orchestration behavior, not
  repo-specific).
- **Routing decision**: **routed** to
  `repo-governance/development/agents/subagent-orchestration.md` §Anti-Patterns — added a "Debounce
  before resuming" addendum to the existing "Delegating an Open-Ended Poll Loop Inside a Long Chunk"
  entry.

---

## Learning: self-hosted-runner CI can take many poll cycles to clear even when nothing is actually stuck

- **Context**: the ose-infra PR #6 CI run on the final fixer commit took roughly 8 consecutive
  ~270-second poll cycles (well over 30 minutes of wall-clock) to go from the first passing checks to
  fully green, with checks turning green a few at a time rather than in a burst.
- **Observation**: this matches the already-known, already-tracked self-hosted-runner capacity
  behavior (see the existing project note on rustup-concurrency contention on the runner) rather than
  revealing anything new. A backlog plan for CI runner-health monitoring was already created in
  Phase 6 (see `plans/backlog/`) to track the underlying infrastructure question.
- **Litmus**: FAILS — no new fact; an existing tracked issue with an existing backlog item.
- **Routing decision**: **discarded** — reason: duplicate of already-tracked infra behavior; the
  Phase 6 ose-infra CI-runner-health backlog plan is the correct home, and it already exists.

---

## Summary (Phases 0–5, complete)

| Entry                                                            | Terminal state | Destination                                                                     |
| ---------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------- |
| Fresh agent files not invocable same-session via `subagent_type` | Routed         | `repo-governance/development/agents/ai-agents.md` §Creating New Agents §Testing |
| Background agent stopped mid-poll-loop, needed resume            | Routed         | `repo-governance/development/agents/subagent-orchestration.md` §Anti-Patterns   |
| Final-cycle thoroughness instruction worked as designed          | Discarded      | — (validation, not a new fact)                                                  |
| Link-label/target semantic mismatch bug class                    | Discarded      | — (no clear automatable rule; caught by existing review mechanism)              |
| Single green-CI reading insufficient proof of agent stall        | Routed         | `repo-governance/development/agents/subagent-orchestration.md` §Anti-Patterns   |
| Self-hosted-runner CI slow-clear over many poll cycles           | Discarded      | — (duplicate of already-tracked infra issue + existing backlog plan)            |
