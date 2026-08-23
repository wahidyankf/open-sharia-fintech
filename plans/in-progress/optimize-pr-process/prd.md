# Product Requirements: Optimize the Pull Request Process

## Users

The author explains intent; a coding-bootcamp graduate must be able to follow the change and learn
from review; reviewers cite evidence and impact; fixers appraise claims; maintainers audit merged
history; plan executors preserve authority, scope, and stable delivery across both repositories.

## Functional Requirements

1. PR bodies lead with outcome and why, then scope/non-goals, reading guide, verification, review
   focus, dependency, “feature flag” or integration safety, stable-main proof, and rollback.
2. Useful Mermaid diagrams may clarify three or more relationships. They use accessible colors,
   meaningful labels, and equivalent prose; omit them when a paragraph or table is clearer.
3. A consolidated review stays concise. Each blocking finding names severity, evidence, impact,
   a bounded remedy, and a safe refutation check; teaching notes are visibly nonblocking.
4. Each unresolved finding receives a native same-thread reply with a machine-readable disposition,
   concrete evidence, commit link where applicable, and the exact AI footer.
5. Fixers choose `fix`, `reject-with-reason`, `defer-with-reason`, or `clarify`; only genuinely
   addressed threads resolve. Rejections engage the evidence, not the reviewer’s authority.
6. Scope is frozen at review start. Same-defect completeness is in scope; unrelated improvement is
   filed separately. No review cycle grows the PR’s promised outcome.
7. Entry readiness, specialist selection, deduplication, one repair batch, and focused rereview
   should converge in Cycles 1–3. Cycles 4–5 document why recovery is still safe; execution stops
   before Cycle 6 without a routine earlier human checkpoint.
8. Plans own requirements, design, delivery order, validation, knowledge capture, and closure. Repo
   rules own durable norms. Code/tests implement behavior. Each moves through its own bounded PR.
9. One named worktree per repository lasts for the whole plan. Dependent PRs are sequential and
   unstacked; each starts from current `origin/main` after the previous dependency merges.
10. Public portable changes open an auditable private obligation pinned to the public PR, merge SHA,
    and reviewed head. One upstream correction is allowed per wave; a second reversal stops as
    oscillation. Private-only defects never trigger public churn.
11. Private-only defects and deliberate deviations stay private. In contrast,
    byte-identity defects follow the existing surface authority; parity repair may require a public
    correction, a private correction, or both under the existing evidence rules.
12. Idea briefs related to this plan retire in later public/private idea-only PRs, with each useful
    requirement mapped here and each discarded item given a short reason.

## Acceptance Criteria

```gherkin
Feature: Human-readable pull-request delivery
  Scenario: A large task spans plans, rules, and code
    Given one plan worktree exists in each affected repository
    When the executor decomposes the delivery
    Then plan, idea, rule, binding, code, and closure concerns use sequential cohesive PRs
    And every dependency merges green before its dependent PR opens
  Scenario: A junior engineer reads a blocking finding
    When the review is posted
    Then the finding explains evidence, impact, and a bounded remedy in plain language
    And optional teaching is clearly nonblocking
  Scenario: A fixer disagrees with a finding
    When the cited evidence does not establish the claim
    Then the fixer replies in the same thread with a reasoned rejection and evidence
    And the reply ends with the AI marker
  Scenario: Review converges normally
    Given Cycle 1 began from a complete description and green local checks
    When verified findings are repaired as one coherent batch
    Then focused rereview should finish by Cycle 3
    And no new outcome enters scope
  Scenario: Review does not converge
    Given Cycle 5 still has a merge-blocking finding
    When another cycle would be required
    Then automation stops before Cycle 6 and leaves a human-readable escalation on the PR
  Scenario: Private review finds byte-identity drift
    When the affected surface has an existing byte-identity contract
    Then repair follows that surface's authority and records parity evidence
    And the one-correction and oscillation bounds still apply
```

## Non-Functional Requirements

All records remain readable after merge, links use stable PR/SHA anchors, diagrams meet accessible
contrast, secrets and identities remain untouched, and no new tool or CI gate ships without a
documented necessity decision and regression evidence.
