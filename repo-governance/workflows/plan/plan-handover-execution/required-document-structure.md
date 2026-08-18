---
title: "Required Document Structure"
description: The contractual section shape every handover uses.
when_to_use: Use as the template for a handover's section structure.
---

# Required Document Structure

Every handover document uses this exact section shape, in this order — not a suggestion, a contract.
The read side ([`plan-takeover-execution.md`](../plan-takeover-execution.md) A0.5) is a human or an
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

Continued in
[Notes and Execution Mode](./notes-and-execution-mode.md).
