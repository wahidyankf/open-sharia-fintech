# Product Requirements — Merge-Queue Adoption

## Product Overview

Adopt a **GitHub-native merge queue** (D10, currently re-opened by MQ-1) to harden
**merge-precondition (c)** under concurrent `worktree-to-pr` integration. The product surface is
CI-workflow YAML, governance/protocol markdown, and a per-repo `[HUMAN]` enablement runbook — there is
no runtime code. Adoption is **gated on a per-repo availability matrix** (Phase 0), because
merge-queue availability depends on repository **owner type** (organization vs personal account) —
verified today as unavailable for all three repos, which surfaces decision **MQ-1**.

## Personas (hats the maintainer wears; consuming agents)

- **The Availability investigator** — needs to know, per repo, whether the platform exposes a
  merge-queue toggle at all (owner type: organization vs personal account — the real gate), verified
  rather than assumed.
- **The CI author** — needs the `merge_group` trigger added to exactly the workflow(s) that must gate
  the speculative merge, reusing the existing `pull_request` jobs so queued CI matches branch CI.
- **The Governance author** — needs precondition (c) reworded to be **satisfiable by the queue** while
  keeping the **manual fallback** for branches/repos without one, with (a)–(e) lettering preserved.
- **The Maintainer enabling the queue** — performs the `[HUMAN]` repo-settings toggle and confirms it;
  an agent must never change repository security settings.
- **`plan-execution` + the PR-Review Cycle agents (consuming)** — the 3-cycle Maker→Fixer loop and the
  five-precondition merge gate must survive unchanged; only (c)'s _satisfaction path_ changes.

## User Stories

- **US-1** — As the availability investigator, I want a per-repo merge-queue availability matrix
  keyed on **owner type** (organization vs personal account — the actual GitHub-documented gate, not
  visibility or plan tier), so that adoption targets only repos where the queue actually exists.
- **US-2** — As the CI author, I want a `merge_group` trigger on the gating workflow(s), so that CI runs
  on the speculative merge result and an evicted PR never lands on `main`.
- **US-3** — As the governance author, I want precondition (c) reworded to be satisfiable by the queue
  with a retained manual fallback, so that queue-enabled and non-queue branches both have a defined path.
- **US-4** — As the maintainer, I want the queue enabled via a `[HUMAN]` runbook bracketed by `[AI]`
  prep and `[AI]` `gh api` verification, so that no agent ever changes repository security settings.
- **US-5** — As a consuming plan-execution run, I want the 3-cycle review loop and the five merge
  preconditions preserved verbatim, so that adopting the queue changes only how (c) is satisfied.
- **US-6** — As the maintainer relying on `[AI]` automerge, I want the automerge-via-queue path
  documented, so that the `[AI]`-merges-by-default posture keeps working once a queue is active.
- **US-7** — As the parity owner, I want the shared CI-trigger + protocol scaffolding delivered to all
  three repos with **enablement branching on MQ-1 per repo**, so that the shared organization-ownership
  blocker (identical across all three today) defers only the enablement step, not the scaffolding
  deliverable — and any repo that later gains an org owner can enable independently.

## Acceptance Criteria

Each acceptance criterion follows the step-keyword cardinality HARD rule: exactly one primary `Given`,
one `When`, one `Then`; extras chain with `And`/`But`.

### AC-1: A per-repo availability matrix is recorded before any adoption

```gherkin
Scenario: Merge-queue availability is investigated per repo
  Given merge-queue availability is gated by repository owner type (organization vs personal account), not by visibility or plan tier
  When Phase 0 investigates availability via web-researcher and a gh api owner.type probe on each repo
  Then a matrix records, per repo, whether the merge queue is available
  And each entry cites its evidence source (GitHub docs plus the gh api owner.type probe)
  And any repo where the queue is unavailable surfaces the MQ-1 ownership-fork decision instead of a per-repo deferral
```

### AC-2: The gating workflow triggers on the speculative merge

```gherkin
Scenario: CI runs on the merge_group event
  Given the CI workflow that must gate the merge previously triggered only on pull_request and push
  When the merge_group trigger is added to that workflow in an adopting repo
  Then the workflow lists merge_group among its on: events
  And the merge_group run reuses the same jobs as the pull_request run
  And actionlint passes on the modified workflow
```

### AC-3: Precondition (c) is satisfiable by the queue with a manual fallback

```gherkin
Scenario: The protocol reword preserves the gate while adding a queue path
  Given pr-merge-protocol.md defines five hardened preconditions lettered (a) through (e)
  When precondition (c) is reworded for merge-queue satisfaction
  Then (c) is documented as satisfied by the queue's speculative merge where a queue is enabled
  And (c) retains the manual non-destructive branch-up-to-date form as the fallback where no queue exists
  And preconditions (a), (b), (d), (e) and the (a)-(e) lettering are unchanged
```

### AC-4: The queue serializes concurrent integration and evicts failures

```gherkin
Scenario: Two concurrently-ready PRs integrate through the queue
  Given the merge queue is enabled in a repo and two worktree-to-pr PRs are ready to merge concurrently
  When both are added to the queue
  Then the queue serializes their integration with CI on each speculative merge result
  And a PR whose queued CI fails is auto-evicted without breaking main
  And each PR remains an independent merge point, preserving the 1-PR-to-1-worktree model
```

### AC-5: Enablement is a `[HUMAN]` step an agent never performs

```gherkin
Scenario: The queue is enabled by a human and verified by an agent
  Given the merge-queue settings live under repository branch protection or rulesets
  When the enablement phase runs
  Then an agent prepares the exact settings runbook but does not change any repository setting
  And a human enables the queue per the runbook
  And an agent then verifies the queue is active via gh api
```

### AC-6: The `[AI]` automerge default works through the queue

```gherkin
Scenario: Automerge adds the PR to the queue instead of merging directly
  Given the repo default is [AI] automerge once the five preconditions hold
  When an [AI] actor finalizes a queue-enabled PR
  Then the operations doc specifies the automerge-via-queue path
  And the PR is added to the merge queue rather than fast-merged past it
  And the merge completes only after the queued speculative CI passes
```

### AC-7: The scaffolding reaches all three repos with conditional enablement

```gherkin
Scenario: Shared scaffolding propagates while enablement respects availability
  Given the merge_group trigger and the precondition-(c) reword have merged to ose-public main
  When the propagation phases deliver the identical scaffolding to ose-primer and ose-infra, each via its own worktree-to-pr cycle
  Then all three repos carry the shared CI-trigger and protocol/doc scaffolding
  And the queue is enabled in every repo where the availability matrix says it is available
  But any repo where the queue is unavailable carries a written conditional deferral with a resume signal
  And no rhino-cli file is touched in any repo, preserving the rhino-cli byte-identity boundary
```

## Product Scope

**In scope (features)**:

- A per-repo merge-queue **availability matrix** (Phase 0 investigation output).
- A `merge_group` **CI trigger** on the gating workflow(s) in each adopting repo's `.github/workflows/`.
- A **precondition-(c) reword** in `pr-merge-protocol.md` (queue-satisfiable + manual fallback;
  (a)–(e) lettering preserved).
- A **merge-queue operations doc** (queue × 3-cycle review × `[AI]` automerge × 1-PR↔1-worktree).
- A per-repo `[HUMAN]` **enablement runbook**, bracketed by `[AI]` prep + `[AI]` `gh api` verification.
- **Three-repo parity** of the scaffolding, with **enablement conditional per repo** on the matrix.

**Out of scope (features)**:

- Any `apps/`/`libs/` runtime code.
- The PR-reviewer decomposition (owned by `worktree-to-pr-hardening`).
- Deciding MQ-1 (organization migration, third-party queue, non-queue hardening, or deferral) — a
  `[HUMAN]` ownership/vendor decision this plan surfaces but does not make.
- Changing preconditions (a), (b), (d), (e).
- Provisioning a bot/GitHub-App identity.

## Product-Level Risks

- **Organization-ownership unavailability** — confirmed today for **all three** repos (personal
  (User)-owned; owner type, not visibility, is the gate). Mitigated by the Phase 0 owner-type-first
  matrix and by surfacing decision MQ-1 rather than assuming a per-repo deferral (AC-1, AC-7).
- **Automerge regression** — `[AI]` automerge must add-to-queue, not bypass it. Mitigated by the
  operations doc + dogfooding on this plan's own PRs (AC-6).
- **Queued CI ≠ branch CI** — the `merge_group` job set must match `pull_request`. Mitigated by reusing
  the same jobs + the `actionlint` gate (AC-2).
- **Settings-change temptation** — enablement is `[HUMAN]`-only. Mitigated by the hard rule +
  `[AI]`-verify-only posture (AC-5).

The **factual claims / judgments** behind these risks live in
[brd.md §Business Risks](./brd.md#business-risks-and-mitigations); the testable scenarios are the ACs
above.
