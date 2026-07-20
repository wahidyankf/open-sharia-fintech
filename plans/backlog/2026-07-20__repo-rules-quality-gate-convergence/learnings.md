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

## Learning: a guard belongs at the point of rewrite, not in a section reached only by suspicion

- **Context**: the PR-review maker→fixer cycles on PR #78, where four consecutive fixes each
  introduced the next defect while every guard was correct on the axis it named.
- **Observation**: the axis sequence was tag value (`[HUMAN]` covered, `[HUMAN → AI]` not), verb
  (writing `[AI]` forbidden, deleting the step not), delivery mode (`*-to-pr` only), confidence
  level (HIGH auto-apply path unguarded), and finally finding type. The last is structural rather
  than a wording miss: `.claude/agents/plan-fixer.md`'s umbrella guard claims to bind "no recipe in
  this file, present or future" and **is true on its own terms**, but every enforcement pointer in
  that file is indexed by plan-checker finding type, and §Execution-Grade Clarity Fixes has none. It
  fires on "checkbox lacks file path / verbatim command / acceptance criterion", auto-applies at
  HIGH confidence, and a step reading `- [ ] [HUMAN] Merge PR once all preconditions hold` has none
  of the three. It derives `gh pr merge`, after which two other rules push the step toward `[AI]`.
  A fixer entering on that finding type never reaches the guard — the human merge gate could be
  stripped by a rule about missing file paths, which never mentions merging.
- **Why it might generalize**: enumerating axes failed four consecutive times, so the fix is
  **placement**, not a longer enumeration. Two durable rules follow: a guard is co-located with
  every rewrite that could violate the invariant, and guard coverage is verified by enumerating how
  an agent **enters** the file (finding type, step number) rather than by reading what each section
  claims to cover. Generalized as the **enumeration-fails-open rule**: any safety property expressed
  as an enumeration fails open on the member nobody listed; prefer properties expressed by what they
  protect over what they enumerate. Recorded as DECISION 9 / DD-9; BS-12 and BS-15 are two further
  instances. Strong candidate for the maker-checker-fixer pattern convention repo-wide.

## Learning: `grep` here is ugrep, and a rejected flag plus `2>/dev/null` fakes a clean sweep

- **Context**: re-verifying sweep evidence while integrating the PR-review session's findings.
- **Observation**: `grep` resolves to **ugrep**, which REJECTS ripgrep's `--glob`. Combined with
  `2>/dev/null`, a hard command failure is indistinguishable from a genuine zero-result sweep.
  Measured on one pattern in one tree: `grep -rn --glob '*.md' PATTERN . 2>/dev/null` returned
  **0**; `command grep -rn --include='*.md' PATTERN .` returned **543**;
  `/opt/homebrew/bin/rg -c --glob '*.md' PATTERN` returned **147 files**. A related trap of the same
  shape: `ls` output carries hyperlink escape sequences that eat leading characters and silently
  corrupt a catalogue diff — precisely the diff BS-13/BS-14 detection depends on.
- **Why it might generalize**: this invalidates any "swept and found nothing" conclusion produced
  that way, across every checker and fixer in the repo, and it is silent. The normative form is that
  **a sweep's zero is evidence only if the command could have produced a non-zero result**: record
  the verbatim command, never suppress stderr, use POSIX `--include` or `/opt/homebrew/bin/rg` by
  absolute path, and run a known-positive control probe before trusting the zero. Use `find -print0`
  for catalogue enumeration. Recorded as DECISION 10 / DD-11. Candidate rule for the
  repository-validation convention and for every checker agent's evidence contract.

## Learning: completeness-diff reaches defects no text search can reach, and ground truth is not always a file

- **Context**: the PR-review session, which surfaced BS-13, BS-14 and BS-15.
- **Observation**: all three were invisible to text search by construction. BS-13 was an incomplete
  description containing none of the swept terms and linking nowhere; BS-14 was an artifact present
  on disk and absent from every catalogue, so there was neither text to match nor a link to follow;
  BS-15 was a safety rule scoped by an enumeration whose ground truth is `git branch -r` — 11 live
  environment branches against a table covering 8, leaving three deploy targets uncovered by a
  "never commit directly" rule, one of which an agent force-pushes to. All three were found by
  enumerating ground truth and diffing it against the document claiming to describe it.
- **Why it might generalize**: the mechanism (completeness-diff) is domain-independent and found
  one-fifth of the registry in a single session. Its rider is what makes it correct: **ground truth
  is sometimes not a file on disk**, so a contract that silently assumes on-disk artifacts
  reproduces BS-15 rather than catching it. Recorded as DECISION 11 / DD-10. Also worth recording
  that **classes compose** — BS-15 is simultaneously a BS-11 instance, since a byte-budget trim
  replaced an inline enumeration with a pointer to an incomplete table.

## Learning: fixed cycle counts and resolved threads are both proxies that fail

- **Context**: the PR-review maker→fixer cycle on PR #78.
- **Observation**: two independent proxy failures. First, all three default cycles found blocking
  defects and **two further verification passes after cycle 3 each found another** — the loop was
  still productive when arithmetic declared it done. Second, a fixer instructed not to touch
  `AGENTS.md` (instruction-size budget) correctly left the orchestrator's HIGH fix uncommitted in
  the working tree, replied to the thread explaining why, and **resolved** it; GitHub then reported
  0 unresolved threads while the blocking defect was absent from the PR. A third, unfixed here:
  `pr-review-maker` cannot post `REQUEST_CHANGES` (`gh` authenticates as the PR author and GitHub
  rejects self-review state changes), so reviews post as `COMMENT` and any gate reading review
  **state** sees the PR as unblocked.
- **Why it might generalize**: all three are the same shape as the plan's thesis — a terminal
  verdict resting on a proxy rather than the property it stands for. Termination should be
  evidence-based (a cycle finding nothing new) rather than count-based, and merge preconditions
  should verify fixes are committed and pushed rather than that threads are closed. A further
  corollary observed the same session: a verification prompt must **license a negative finding** —
  one reviewer told "assume the previous fix introduced a defect" reported the hypothesis wrong and
  found a real defect elsewhere; a prompt without that license manufactures agreement. Recorded as
  DECISIONs 12 and 13 / DD-12 and DD-13; the `REQUEST_CHANGES` gap is filed as a separate backlog
  plan during Knowledge Capture.
