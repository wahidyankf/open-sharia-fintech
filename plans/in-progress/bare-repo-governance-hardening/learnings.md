<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: bare-repo-governance-hardening

Append one `## Learning: <one-line summary>` section per generalizable observation, sanitized per
the secret/sensitivity gate before it is ever written. Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to `<path>` / filed as `plans/backlog/<slug>/` / discarded — `<reason>`
```

> **Watch for this plan's own highest-yield source**: Phases 4 and 5 execute the very procedure
> `bare-repo-landing-method.md` documents. Any friction between the written steps and what execution
> actually required is a defect in that document — record it here, and Phase 6 routes it back into
> the document in all three repos.
>
> If execution surfaces nothing generalizable, replace this line with the explicit escape:
> `No generalizable learnings — <one-line reason>`. Never leave the file silently empty.

## Learning: the defect reproduced live during this plan's own promotion

- **Context**: promoting the plan from `backlog/` to `in-progress/` on 2026-07-21, re-verifying the
  repo-grounded claims in `tech-docs.md` before running the quality gate.
- **Observation**: both bare siblings read `2 0` on
  `git rev-list --left-right --count origin/main...main` — local `main` two commits behind
  `origin/main` in each. The lagging commits (`c12e1eb7f` + `53d9081b7` in `ose-primer`,
  `474545a69` + `f6ecdcc0b` in `ose-infra`) were landed through side worktrees in an earlier
  session. Nothing failed and nothing warned; the lag is only visible if you ask for it explicitly.
  `tech-docs.md` had recorded `0 0` for both, so the plan's own written state had silently gone
  stale in under a day.
- **Why it might generalize**: this is the plan's motivating failure class, observed without being
  sought, on a repo whose maintainer already knows about it. It is direct evidence for the strength
  of C1's terminal-reconcile step — a rule that is easy to forget is not adequately served by prose
  alone, which is worth weighing against **DD-2**'s no-automation stance at Phase 6 triage.
  It also shows any "verified state" line in a plan needs a re-verification step, not just a date.
- **Terminal state**: pending — triage at Phase 6. Candidate route: a worked example inside `C1`
  showing the non-zero reading and the `git fetch origin main:main` recovery.

## Learning: varying the approach each iteration makes a stability-based termination rule unreachable

- **Context**: running `plan-quality-gate` on this plan before execution. The gate terminates on
  **two consecutive zero-finding iterations** and caps at 7 iterations, escalating at 5.
- **Observation**: each iteration was briefed to **vary its approach** so it would not simply repeat
  the last one. The gate then ran 5 (2 MEDIUM), 6 (1 HIGH), 7 (zero) and hit the budget with
  `consecutive_zero_count = 1` — closed at zero outstanding findings, but by exhaustion rather than
  by convergence. The termination rule tests stability by asking whether an **equivalent** check
  returns zero twice running; a deliberately different check each round measures coverage instead, so
  two consecutive zeros were structurally impossible no matter how clean the plan got.
- **Why it might generalize**: it is a general defect in how a saturation loop is driven, not
  specific to this plan. Varying the approach and testing for stability are both individually sound
  and jointly incoherent — the fix is to sequence them (vary while findings are still arriving, then
  hold the approach fixed once a round comes back clean, so the confirming round is genuinely
  equivalent), not to drop either. The same shape applies to any loop-until-dry harness whose exit
  condition counts consecutive empty rounds.
- **Terminal state**: pending — triage at Phase 6. Candidate route:
  `repo-governance/workflows/plan/plan-quality-gate.md`, as a constraint on how iterations are
  briefed rather than a change to the exit condition itself.

## Learning: a checker without the tool its acceptance clauses name will substitute silently

- **Context**: Phases 2 and 3 were executed by agents whose toolset was `Read`/`Write`/`Edit`/
  `Glob`/`Grep` — no `Bash`. Every acceptance clause in those phases names a literal shell command.
- **Observation**: both agents substituted the `Grep` tool's count mode for `grep -Fc` and reported
  the results as the clause's `Result`. Both disclosed the substitution in a tooling note, which is
  the good outcome. But the substitution was **not uniform in reach**: neither could run
  `rhino-cli`/`markdownlint-cli2` at all, so the markdown gates were skipped entirely for the phase —
  and because their disclosed lint runs covered `repo-governance/` but not `plans/`, five
  markdownlint violations reached the pre-commit hook undetected in `delivery.md` itself.
- **Why it might generalize**: the failure is not "the agent lacked a tool" — it is that an
  acceptance clause naming a shell command reads as satisfied when a **differently-scoped**
  substitute returns a plausible number. A phase whose gate is defined in shell commands needs its
  executor's tool grant checked against those commands up front, and any phase that edits markdown
  needs its lint scope to cover **every** path it edited, not just the phase's headline directory.
- **Terminal state**: pending — triage at Phase 6. Candidate routes:
  `repo-governance/development/agents/subagent-orchestration.md` (match the tool grant to the
  acceptance clauses when briefing) and `repo-governance/development/pattern/maker-checker-fixer.md`
  (a disclosed substitution is not a discharged check).

## Learning: Phase 4/5's file-agreement steps do not name `<GATE>`, which cycle 1 turned into a real edit site

- **Context**: PR-review cycle 3 (final) reversed cycle 1's floor-not-ceiling fix to
  `pr-review-quality-gate.md` (`<GATE>`) into a hard-ceiling-not-floor fix, per an explicit user
  ruling. Re-deriving every site touching this rule (per the cycle-3 fixer brief) required rereading
  Phase 4 and Phase 5 in full.
- **Observation**: `<GATE>`'s Path Constants entry (`delivery.md` — the `<GATE>` bullet) still
  describes it as a "source note ... originally left unedited, corrected during PR-review cycle 1,"
  but Phase 4's and Phase 5's propagation steps only name `<MERGE>`, `<PARITY>`, `<PLANS>`, `<SDLC>`,
  `<PROMO>` for the sibling-agreement diff (the "verify the remaining five files agree" step) — never
  `<GATE>`. Since cycle 1 already made `<GATE>` a real `ose-public`-only edit, and cycle 3 edits it
  again, Phase 4/5 as currently written would propagate `<MERGE>`/`<PLANS>`/etc. but silently leave
  the siblings' copies of `<GATE>` un-diffed against the corrected `ose-public` version — nothing
  in Phase 4 or Phase 5 as written would catch a stale sibling `<GATE>`.
- **Why it might generalize**: a source-of-truth file that starts as "read-only, never edited" and
  later becomes a real edit site (as `<GATE>` did across two review cycles) needs its propagation
  bookkeeping updated at the same time the "unedited" claim is retracted — the retraction and the
  propagation-list update are two different edits to two different places, and it is easy to make
  the first without the second.
- **Terminal state**: pending — triage at Phase 6. Candidate route: before Phase 4 executes, add
  `<GATE>` to the C5-propagation steps (Phase 4 and Phase 5) and to the "remaining five files agree"
  step (which becomes six), mirroring how `<MERGE>` is already handled — this is a correction to
  Phase 4/5's own step list, not yet executed, so it can land as an ordinary edit rather than a
  reopened-and-corrected retrospective note.
