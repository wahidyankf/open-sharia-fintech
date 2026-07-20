<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: repo-rules-quality-gate-convergence

## Learning: the plan's own evidence SHAs are perishable, and nearly became blind-spot class 11

- **Context**: relocating this plan from the evidence worktree to the primary checkout during
  authoring, and re-verifying every pre-edit acceptance value against `main`.
- **Observation**: the twelve corrective commits that constitute this plan's entire evidence base
  live on the unmerged branch `parallel-orchestration-shared-machine-governance` (tip `434430e0f`),
  not on `main` — `git merge-base --is-ancestor c30ac344e origin/main` returns non-zero, and both
  `main` and `origin/main` sit at `a207b66e7`. Because this repo squash-merges PRs, every cited SHA
  will stop resolving the moment that branch lands. The first draft cited SHAs as the sole evidence,
  which would have produced a registry that silently became unverifiable — a self-inflicted instance
  of the very blind-spot class (BS-11) the registry catalogues.
- **Why it might generalize**: any governance document whose authority rests on commit SHAs is
  fragile under squash-merge. The general rule is that durable documentation embeds its evidence
  inline and treats the SHA as a convenience pointer. This is recorded as DECISION 8 and DD-8, and is
  a candidate rule for the plan-anti-hallucination or knowledge-capture conventions.

## Learning: pre-edit acceptance values must be measured in the checkout the plan will execute from

- **Context**: the plan was drafted while working inside the evidence worktree, whose tree already
  contains the twelve corrective commits.
- **Observation**: every "returns 0 today" claim was originally measured against the worktree's tree,
  which is 12 commits ahead of `origin/main` on governance content. Re-measuring all of them against
  `main` at `a207b66e7` happened to confirm identical values, but that was luck rather than method —
  several of the touched files (`.github/workflows/main-ci.yml` among them) differ between the two
  trees, and the CI mermaid invocation this plan quotes sits at line 113 on `main` versus line 114 on
  the branch.
- **Why it might generalize**: a plan's acceptance clauses are executed from a worktree provisioned
  off `origin/main`, so authoring-time measurements taken anywhere else are not evidence about the
  execution environment. Citing a file path rather than a line number is the cheap mitigation. This
  is a candidate addition to the plan-anti-hallucination convention's verification recipes.

## Learning: a validator's own negative fixtures are an evidence trap for any checker

- **Context**: analysing the false alarm in the archived chain while authoring Phase 4.
- **Observation**: `md mermaid validate` invoked bare flags four violations that are the validator's
  own deliberately-invalid fixtures. CI invokes it with
  `--exclude apps/rhino-cli/tests/fixtures --exclude plans/done`
  (`.github/workflows/main-ci.yml`), whereas the `package.json` lint-staged entry uses the bare form —
  so an agent copying the convenient local invocation gets a different answer from CI. Acting on it
  would have manufactured work inside the `apps/rhino-cli` byte-identity boundary, a three-repository
  blast radius from a phantom defect.
- **Why it might generalize**: this is not specific to mermaid. Any validator that ships negative
  fixtures has two invocation forms with different truth values, and the repo currently has no rule
  requiring evidence-producing invocations to match CI's. Encoded here as DD-5 rule B; the general
  form is a candidate rule for the repository-validation convention.
