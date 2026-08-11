# Product Requirements: PR Review Rule Convergence

## Product Overview

This policy is the repository's deterministic decision surface for reviewing and merging pull
requests. It gives every agent one route for executable changes and a lightweight route for
non-executable changes, independent of whether a plan initiated the delivery.

## Personas

- **Maintainer**: needs a predictable merge decision without running expensive review work for prose.
- **PR-review orchestrator**: must route a PR deterministically and retain evidence for the chosen path.
- **Repo-rules maker**: must apply the same rule coherently to governance documentation and generated
  harness bindings.

## User Stories

- As a maintainer, I want a code-affecting PR to receive a bounded, substantive review loop so it is
  safe to merge without routine human approval.
- As a maintainer, I want a prose-only PR to merge after the named CI workflow so routine documentation
  work is not delayed by irrelevant specialist review.
- As a security responder, I want a confirmed leak to use a documented full-history response so the
  exposed value is not retained in reachable repository or PR history.

## Acceptance Criteria

### Eligible PR exits early

```gherkin
Scenario: An executable PR reaches a clean review state before the ceiling
  Given an open PR with an executable artifact in its diff
  And its latest completed cycle has no unresolved code-related Medium, High, or Critical finding
  When the orchestrator evaluates the cycle result
  Then it stops the specialist cycle without starting another pass
  And it may merge only after the configured quality workflow is green
```

### Eligible PR fails to converge

```gherkin
Scenario: An executable PR still has a qualifying code finding at cycle seven
  Given an open eligible PR has completed seven sequential cycles
  And a code-related Medium, High, or Critical finding remains
  When the merge preconditions are evaluated
  Then the PR is not merged
  And cycle-six-or-later learning evidence and any reusable improvement idea are recorded
```

### Non-eligible PR follows the lightweight route

```gherkin
Scenario: A prose-only PR is ready to merge
  Given an open PR changes no executable artifact
  And .github/workflows/pr-quality-gate.yml has succeeded for its head commit
  When the merge route is evaluated
  Then the specialist PR-review cycle is skipped
  And the PR is merged unless universal secret handling blocks it
```

### Open PRs transition immediately

```gherkin
Scenario: A PR was open when the policy landed
  Given a PR predates the policy merge
  When it next enters a review or merge action
  Then the orchestrator classifies its current diff under the new routing rule
  And it does not retain a legacy review path
```

### Runner contention preserves the active goal

```gherkin
Scenario: A PR workflow is queued because runners are contended
  Given the PR's current-head quality workflow is queued or stalled
  When the agent monitors the workflow
  Then it retains the active goal
  And it investigates cross-repository runner contention at the documented cadence
  And it does not cancel the goal solely because runner capacity is unavailable
```

### The OSE-private companion uses its one-plan direct-push exception

```gherkin
Scenario: This plan's OSE-private companion is ready to deliver
  Given the companion's expected head and public/private byte-identity manifest are verified
  And no secret incident blocks the delivery
  When the public canonical revision has merged
  Then the agent commits and pushes the private worktree directly to origin main
  And it does not extend that exception to another repository, workflow, or plan
```

### Completion removes the exact plan worktree

```gherkin
Scenario: A repository has completed this plan's final delivery
  Given every delivery unit for that repository is merged or pushed
  And the repository has no uncommitted or unpushed plan change
  When the executor completes its post-delivery verification
  Then it removes the exact worktree used by this plan immediately
  And it retains the repository root checkout for final origin main synchronization
```

### AI completes the entire delivery

```gherkin
Scenario: The plan reaches a delivery or verification boundary
  Given all required evidence for the boundary is available to the agent
  When the next task is selected
  Then the agent performs the task and its verification without a human approval gate
  And it records the result in the persistent delivery checklist
```

### Confirmed secret leak replaces a PR

```gherkin
Scenario: A real secret is confirmed in an open PR history
  Given the secret is contained and rotated without exposing its value in evidence
  When affected reachable refs are identified
  Then each affected ref is rewritten under the standing incident authorization
  And the contaminated branch and PR are replaced with a clean branch and PR
  And provider purge support is requested without claiming external copies were erased
```

## Product Scope

The rule covers all planned and ad-hoc PR delivery work. A text change only becomes review-eligible
when its content itself controls behavior, such as a workflow, script, runtime configuration, or
validation registry; its filename extension or plan origin does not decide eligibility.

### In Scope

- Review classification, bounded review cycles, merge routing, convergence learning, secret response,
  runner-contention handling, plan-worktree cleanup, and cross-repository propagation.

### Out of Scope

- Application features, UI/API behavior, external clone deletion, and a reusable direct-push exception
  for non-private deliveries.

## Product Risks

- A classifier may be ambiguous for a novel configuration surface; the safe route is eligible review.
- A single-plan delivery exception could be copied into standing governance; it is therefore recorded
  only in this plan and must not be propagated as a canonical rule.
- A delayed or failed cross-repository companion can produce temporary drift; manifests and the defined
  delivery ordering make that drift observable.
