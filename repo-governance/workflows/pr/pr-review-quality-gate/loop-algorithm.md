---
title: "PR-Review Quality Gate — Loop Algorithm"
description: "The pseudocode for the review_pr loop and its five governing rules: fixed N-cycle ceiling, fresh specialists per cycle, full-PR re-review, the hard CI-green gate, and AI-attribution footers."
when_to_use: "Use when tracing the exact control flow of the review loop, or confirming a specific loop rule (e.g. why specialists are fresh each cycle)."
---

# Loop Algorithm

```text
review_pr(PR, maximum_cycles = 7):          # configurable ceiling, default 7, STRICTLY SEQUENTIAL
    route = classify_changed_artifacts(PR)  # eligible | noneligible; ambiguity => eligible
    if route == noneligible:
        require pr_quality_gate_is_green(PR)
        return not-applicable
    prior = []                              # accumulated consolidated findings + resolution state
    for cycle in 1..=maximum_cycles:
        scout = fresh pr-review-scout-maker(pr = PR, cycle = cycle, total_cycles = N, prior = prior)
                       # scout pins this cycle's ONE head SHA
                       # output: head, tier, specialists, context_brief, dismissals
        synthesis_maker = fresh pr-review-synthesis-maker(state = clean, context_brief = scout.context_brief, fed = prior)
                       # scout hands its context_brief to BOTH consumers below — see scout's Output Contract
        raw = fan_out(scout.specialists, context_brief = scout.context_brief, fed = prior)   # CONCURRENT within this cycle
        consolidated = synthesis_maker.synthesize(raw, dedup_against = prior)
                       # dedup + re-categorize + reasonableness-filter + tool-verify
        post consolidated as ONE line-anchored review (Reviews API)
        fixer = pr-review-fixer()
        fixer.resolve(PR)                   # triage, fix, push, reply, cause-tag each disposition
        wait_until CI_is_GREEN(PR)          # HARD gate before decision or next cycle
        prior += consolidated + their resolution state
        unresolved = outstanding_code_findings(prior, severities = [MEDIUM, HIGH, CRITICAL])
        # outstanding = thread still unresolved. A deferral leaves the set only
        # once its follow-up is filed AND linked, which is what lets it resolve.
        if unresolved is empty and probe_class_is_new(cycle, prior):
            if previous_cycle_was_clean_under_a_new_class(prior):
                return done             # second consecutive clean cycle; LOW findings never hold the loop open
        if cycle % 3 == 0:
            convergence_checkpoint(prior)   # continue | change fix strategy | block
        if cycle >= 6:
            capture_nonconvergence_learning_and_idea(PR, cycle, unresolved)
    return blocked                           # ceiling reached with code M/H/C still outstanding
```

- **Up to N cycles, default 7, strictly sequential** — fan-out→synthesize→fixer, repeated only
  until a clean exit or the configured ceiling,
  never parallel **across** cycles (the specialist fan-out WITHIN a single cycle is concurrent — see
  [Participants](./participants.md#participants)).
- Each cycle spawns **fresh** specialist instances, tier-selected per
  [PR Reviewer-Discipline Convention §Risk-tier fan-out](../../../development/quality/pr-review-disciplines/cost-control-noise-control-mechanics-risk-tier-fan-out.md#risk-tier-fan-out-d12)
  (clean context) fed the coordinator's own prior consolidated findings and their resolution state,
  so the fan-out does not repeat already-posted comments.
- `pr-review-synthesis-maker` reviews the **full PR each cycle** (deduplicating against
  already-posted comments) and MUST explicitly re-review the fixer's new commits from the previous
  cycle, to catch fix-induced regressions.
- **Full CI must be GREEN after the fixer's push** before the next fan-out cycle starts — this is a
  hard gate, not a soft check.
- Every agent ends every comment/reply with the AI-attribution footer in its canonical shape — see
  [Identity and Quality Gates](../../../../.claude/skills/pr-review-fixer-resolution/reference/identity-and-quality-gates.md) —
  since no dedicated bot/GitHub App identity is provisioned; any agent may call `web-researcher` for
  external facts while reviewing, synthesizing, or answering.

See [Pipeline Diagrams](./pipeline-diagrams.md) for the sequence diagram of one cycle.
