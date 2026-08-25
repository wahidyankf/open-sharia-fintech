---
title: "PR-Review Quality Gate — Loop Algorithm"
description: "The pseudocode for the review_pr loop and its five governing rules: fixed N-cycle ceiling, fresh specialists per cycle, full-PR re-review, the hard CI-green gate, and AI-attribution footers."
when_to_use: "Use when tracing the exact control flow of the review loop, or confirming a specific loop rule (e.g. why specialists are fresh each cycle)."
---

# Loop Algorithm

```text
review_pr(PR, maximum_cycles = 5):          # repository ceiling, per-PR extension only
    route = classify_changed_artifacts(PR)  # eligible | noneligible; ambiguity => eligible
    if route == noneligible:
        require pr_quality_gate_is_green(PR)
        return not-applicable
    history = rehydrate_PR_review_history(PR) # ordinal/ceiling, probes, findings/dispositions,
                                              # clean streak, checkpoints
    require_well_formed(history)
    prior = history.findings_and_resolutions
    for cycle in history.next_ordinal..=maximum_cycles:
        scout = fresh pr-review-scout-maker(pr = PR, cycle = cycle, total_cycles = N, prior = prior)
                       # scout pins this cycle's ONE head SHA
        write_or_refresh_pr_body_route_record(route, scout)
        synthesis_maker = fresh pr-review-synthesis-maker(state = clean, context_brief = scout.context_brief, fed = prior)
                       # scout hands its context_brief to BOTH consumers below — see scout's Output Contract
        raw = fan_out(scout.specialists, context_brief = scout.context_brief, fed = prior)   # CONCURRENT within this cycle
        consolidated = synthesis_maker.synthesize(raw, dedup_against = prior)
                       # dedup + re-categorize + reasonableness-filter + tool-verify
        require_live_head_equals(PR, scout.head_sha, boundary = before_review_post)
        post consolidated as ONE line-anchored review (Reviews API)
        require_live_head_equals(PR, scout.head_sha, boundary = before_fixer)
        fixer = pr-review-fixer()
        fixed = fixer.resolve(PR)           # triage, fix, push, reply, cause-tag each disposition
                       # same-defect completion is allowed; unrelated work becomes a linked follow-up
        expected_head = fixed.pushed_head ?? scout.head_sha
        wait_until CI_is_GREEN(PR, head = expected_head)
        require_live_head_equals(PR, expected_head, boundary = before_CI_credit)
        prior += consolidated + their resolution state
        unresolved = outstanding_code_findings(prior, severities = [MEDIUM, HIGH, CRITICAL])
        if unresolved is empty and probe_class_is_new(cycle, prior):
            require expected_head == scout.head_sha # a fix-bearing cycle is not clean
            if previous_cycle_was_clean_under_a_new_class(prior):
                return done             # second consecutive clean cycle; LOW findings never hold the loop open
        if cycle % 3 == 0:
            convergence_checkpoint(prior)   # continue | change fix strategy | block
        if cycle == maximum_cycles:
            capture_nonconvergence_learning_and_idea(PR, cycle, unresolved)
    return blocked                           # ceiling reached, exit condition unmet — with or
                                             # without an outstanding finding; extend per-PR to resolve
```

Hydration, mismatch disposition, and restart accounting are defined in
[Cycle Authority and Restart Recovery](./cycle-authority-and-restart-recovery.md).

- Each cycle spawns **fresh** specialist instances, route-selected per
  [PR Reviewer-Discipline Convention §Risk-tier fan-out](../../../development/quality/pr-review-disciplines/cost-control-noise-control-mechanics-risk-tier-fan-out.md#risk-tier-fan-out-d12)
  and its plans-only override (clean context), fed the coordinator's own prior consolidated findings
  and their resolution state, so the fan-out does not repeat already-posted comments.
- `pr-review-synthesis-maker` reviews the **full PR each cycle** (deduplicating against
  already-posted comments) and MUST explicitly re-review the fixer's new commits from the previous
  cycle, to catch fix-induced regressions.
- **Full CI must be GREEN after the fixer's push** before the next fan-out cycle starts — this is a
  hard gate, not a soft check.
- Every agent ends every comment/reply with the AI-attribution footer in its canonical shape — see
  [Identity and Quality Gates](../../../../.claude/skills/pr-review-fixer-resolution/reference/identity-and-quality-gates.md) —
  since no dedicated bot/GitHub App identity is provisioned; any agent may call `web-researcher` for
  external facts while reviewing, synthesizing, or answering.
