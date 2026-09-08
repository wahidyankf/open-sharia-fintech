---
description: "Composes single review passes with fixer, exact-head CI, and bounded clean credit."
when_to_use: "Use when tracing an explicitly requested iterative PR-review cycle."
---

# Loop Algorithm

```text
review_cycle(PR, maximum_passes = 5):
    require explicit_user_invocation(PR)
    history = authenticate_and_rehydrate_cycle_history(PR)
    require well_formed(history)
    prior = history.findings_and_resolutions

    for ordinal in history.next_ordinal..=maximum_passes:
        probe = choose_unused_probe(history)
        pass = pr_review(PR, probe_class = probe, prior_review_state = prior,
                         delegated_gate_ids, lifecycle_evidence, leak_review_evidence)
        if pass.final_status == failed:
            return blocked
        if pass.final_status == stale:
            record_non_credit(pass, ordinal)
            prior = rehydrate(PR)
            continue

        require authenticate_pass_record(pass.pass_record, pass.review_id, pass.reviewed_head)
        if pass.final_status == findings:
            fixed = pr-review-fixer.resolve(PR, pass.review_id,
                                            delegated_gate_ids, lifecycle_evidence)
        else:
            fixed = no_change(pass.reviewed_head)

        expected_head = fixed.pushed_head ?? pass.reviewed_head
        wait_until aggregate_PR_CI_is_GREEN(PR, head = expected_head, base = applicable_base)
        lifecycle_evidence = exact_head_evidence_or_pending(PR)
        if live_head(PR) != expected_head:
            record_non_credit(pass, ordinal)
            prior = rehydrate(PR)
            continue

        prior += pass.record + current_thread_dispositions
        if pass.final_status == clean and expected_head == pass.reviewed_head:
            emit_and_read_back_positive_credit_v2(ordinal, pass.pass_record,
                                                   immutable_CI_evidence)
            if previous_ordinal_has_adjacent_clean_credit_under_different_probe(prior):
                return done

        if ordinal % 3 == 0:
            convergence_checkpoint(prior)
        if ordinal == maximum_passes:
            capture_nonconvergence_learning_and_idea(PR, ordinal, prior)

    return blocked
```

The cycle preserves its durable ceiling, history, cause tags, probe variation, clean-streak credit,
fixer, and CI behaviour. `pr-review` owns head pinning, risk routing, fan-out, synthesis, the single
`COMMENT` post, and its authenticated `ose-pr-review-pass:v1` record.

The enclosing cycle may invoke a fresh pass after a stale result because the user explicitly chose
the iterative workflow. `pr-review` itself never retries.
