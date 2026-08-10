---
name: plan-handover-execution
title: "plan-handover-execution"
goal: Given an in-progress plan and the current session's execution state, write a structured handover document capturing enough context for a different agent, session, or human to resume the plan without re-discovering already-known state or re-learning the same gotchas
termination: The handover document is written to local-tmp/handovers/, is non-empty, names the plan-identifier and current per-repo state, and its path has been reported back
inputs:
  - name: plan-path
    type: string
    description: Path to the plan folder (in plans/backlog/, plans/in-progress/, or plans/done/) in the current repo, or a bare plan-identifier slug.
    required: true
  - name: date
    type: string
    description: "ISO date (YYYY-MM-DD) to stamp the handover filename with. Defaults to the current date."
    required: false
outputs:
  - name: handover-doc
    type: file
    pattern: local-tmp/handovers/*__*-implementation.md
    default: local-tmp/handovers/<date>__<plan-identifier>-implementation.md
    description: The written handover document. Default filename/folder is `local-tmp/handovers/<date>__<plan-identifier>-implementation.md` — the exact same default `plan-takeover-execution.md`'s Phase A0.5 looks up (see its frontmatter `inputs`/discovery-path note); keep both in sync if this default ever changes.
---

# Plan Handover Execution Workflow

**Purpose**: Capture the state of an in-progress, multi-session, possibly-multi-repo plan into one
document before stepping away from it, so the next agent or session — which starts with none of this
session's context — can resume from fact rather than from re-discovery or guesswork.

**When to use**:

- Ending a session with plan work still in progress, whether by choice, a context/compaction boundary,
  or the user explicitly asking for a handover.
- Before an intentional pause the user has directed (e.g., "pause this phase"), so the pause carries
  forward its own reasoning instead of reading as an unexplained stop next time someone opens the plan.
- Any time a plan's execution is about to move to a different agent, a different session, or a
  different person, and prior context would otherwise be lost.

**When NOT to use**:

- The plan is fully complete — route it through Phase 9/10 (Knowledge Capture, Archival) instead; a
  finished plan needs an archive entry, not a resume document.
- The plan never started — there is no state to hand over; a fresh `plan-takeover-execution.md` run
  on a never-touched plan is already a no-op discovery, per that workflow's own "When NOT to use".

## Relationship to plan-takeover-execution.md (write side / read side)

This workflow is the **write-side counterpart** to
[`plan-takeover-execution.md`](./plan-takeover-execution.md)'s **read side**: that workflow's Phase
A0.5 checks `local-tmp/handovers/` for a document this workflow produces, using it as a fast, informal
lead that narrows and accelerates the git/`gh` ground-truth probes Phase A2 still runs in full — a
handover document is a hint, never a substitute for verification, since it can go stale the moment
another actor touches the same plan. Nothing here duplicates that workflow's discovery logic; this
workflow only produces the artifact it consumes.

## Why This Exists

A plan spanning several sessions and several repos accumulates two kinds of knowledge that
`delivery.md`'s checkboxes alone do not capture:

- **State that isn't a checkbox** — an empty worktree provisioned but not yet used, a PR opened as a
  draft, a pause chosen deliberately rather than forced by an error. `delivery.md` records what's
  _done_; it has no place to record what's _in-progress-but-safe-to-leave_.
- **Gotchas already paid for once** — a branch-protection rule that only reveals itself when a push is
  attempted, a review-cycle escalation rule's exact trigger condition, a tool quirk discovered through
  trial and error. Without a handover, the next session re-discovers each of these the same expensive
  way the first session did.

Skipping a handover when one is warranted risks the same three outcomes
[`plan-takeover-execution.md`](./plan-takeover-execution.md#why-this-workflow-exists) already names
for skipping discovery: re-work, abandoned state, and orphaned leftovers — this workflow prevents them
by making the state explicit before anyone has to go looking for it.

## Required Document Structure

Every handover document uses this exact section shape, in this order — not a suggestion, a contract.
The read side ([`plan-takeover-execution.md`](./plan-takeover-execution.md) A0.5) is a human or an
agent skimming under time pressure; a fixed, predictable shape is what makes a handover **fast** to
consume instead of just informative. A handover missing a required section is incomplete — go back and
fill it in rather than shipping a partial document.

```markdown
# Handover: <plan-identifier>

**Written**: <date>
**Plan-identifier**: `<plan-identifier>`
**Plan folder**: `plans/<stage>/<plan-identifier>/` (in `<repo>`, on `origin/main` or `<branch>`)
**Consuming workflow**: [`plan-takeover-execution.md`](../../repo-governance/workflows/plan/plan-takeover-execution.md)

## One-line status

<One or two sentences: what phase/step the plan is at, and whether it is paused, blocked, or actively
mid-step. This is the sentence a reader stops on if they read nothing else — it must be enough alone
to answer "do I need to read further right now?">

## Per-repo state

### `<repo-name>` — <bucket-style label: e.g. "done, merged" / "in progress, paused" / "untouched">

- Concrete facts only: PR numbers with state (open/draft/merged) and merge commit if merged, branch
  name, worktree path, HEAD commit, uncommitted-changes status. Every claim here must be a fact you
  verified this session, not an assumption — cite the command or evidence if it isn't obvious
  (mirrors A2's "log every hit verbatim" discipline in plan-takeover-execution.md).

<Repeat this subsection once per repo touched or relevant to the plan this session — omit repos with
nothing to report rather than padding with "no changes".>

## What to do next

<Numbered, concrete, actionable steps — name the exact delivery.md step/checkbox to resume at, the
exact command to run first (e.g. a fetch/rebase), and any setup not yet done (e.g. "npm install has
not been run in this worktree"). A reader should be able to start executing from this section without
re-reading anything else in the document.>

## Key gotchas learned this session

<Each gotcha: what happened, why it happened (the mechanism, not just the symptom), and what to do
differently next time. Omit anything already captured in the plan's own tech-docs.md/learnings.md —
this section is for what is NOT yet written down anywhere durable. If nothing non-obvious was
learned, state that explicitly rather than omitting the section.>

## Files this session touched (ledger)

<Either a literal file list, or a pointer to where the full list already lives (e.g. "see PR #N's
diff") if listing every file here would just duplicate that PR. Never leave this section absent —
state explicitly if nothing was touched.>

## Do not re-litigate

<Design decisions, deferred findings, or already-settled debates a fresh reader might otherwise
reopen — one line each, with a pointer to where the decision is recorded (tech-docs.md's decision
table, a specific PR review thread, etc.). Omit this section entirely if nothing applies; do not
force an empty list.>
```

Two sections (**One-line status**, **What to do next**) are load-bearing and must never be empty —
they are what makes the difference between a handover a reader can act on immediately versus one that
requires re-deriving the plan from scratch. The other sections may be legitimately short (a single
sentence, or "nothing to report") but must still be present, so their absence is never mistaken for
"nothing was checked."

## Execution Mode

**Direct Orchestration** — writing one document from state already gathered during the session (or a
short, targeted re-check of current git/PR status) does not warrant a delegated agent.

## Steps

1. **Resolve the plan-identifier and date.** Same resolution rule as
   [`plan-takeover-execution.md` A0](./plan-takeover-execution.md#phase-a--discover-every-trace-of-this-plan-sequential-per-repo-hard-gate):
   the plan folder's bare slug, no date prefix. Default `date` to the current date if not supplied.
2. **Gather current state, per repo touched this session.** For each: worktree path and branch (if
   any), its HEAD commit, whether it has uncommitted changes, any PR number/state/CI status, and the
   `delivery.md` checkbox counts as of now. Prefer state already known from this session's own work
   over re-probing — but if a claim would be stale or uncertain (e.g., "PR is green" from ten minutes
   ago), re-verify rather than assert from memory.
3. **State the concrete next step**, not just the current position — "resume `delivery.md` at
   _[named step]_", not merely "Phase 6 in progress". A handover that describes where things stand but
   not what to do next still forces the reader to re-derive the plan.
4. **Capture non-obvious gotchas learned this session** that are not already written into the plan's
   own `tech-docs.md`/`learnings.md` — a surprising tool behavior, a governance rule that only bites at
   a specific step, a decision the user made live that isn't yet reflected in the plan's committed
   docs. Write the _why_, not just the _what_, exactly as
   [Feedback memory guidance](../../development/quality/knowledge-capture.md) already asks of
   `learnings.md` entries — a future reader needs to judge whether the gotcha still applies, not just
   that it once did.
5. **Write the document** to `local-tmp/handovers/<date>__<plan-identifier>-implementation.md`.
   `local-tmp/` is gitignored — this is a **local, single-machine handoff artifact**, not a
   cross-clone or cross-machine one; it exists to accelerate the _next session on this same disk_, per
   the same same-machine assumption the
   [Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md#parallelism-budget)
   already documents elsewhere. Do not rely on it surviving a fresh clone or a different machine.
6. **If a handover already exists for this plan-identifier from an earlier date, leave it in place.**
   Multiple dated handovers may accumulate; `plan-takeover-execution.md`'s read side picks the
   most recent by filename date. Do not delete or overwrite an older one — it is a historical record of
   what an earlier session believed, useful if a discrepancy ever needs tracing.
7. **Report the written path back** to the user or calling context, and confirm the file is non-empty.

## Related Documentation

- [Plan Takeover Execution](./plan-takeover-execution.md) — the read-side workflow this one's output
  feeds into; owns discovery, reconciliation, and takeover once a handover (or none) is found.
- [Plan Execution](./plan-execution.md) — the workflow a resumed plan ultimately continues in, once
  `plan-takeover-execution.md` has adopted its worktree.
- [Knowledge Capture](../../development/quality/knowledge-capture.md) — the entry-shape convention this
  workflow's gotcha-capture step mirrors, and the destination for a gotcha that turns out to be durable
  rather than session-specific.
- [Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md) —
  the same-machine assumption `local-tmp/handovers/` depends on.
