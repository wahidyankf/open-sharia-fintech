# Product Requirements — Repo Rules Quality Gate Convergence

## Product Overview

Nine coordinated changes to the repo-rules-quality-gate loop and its supporting agents, so the loop
reaches a **trustworthy** zero in fewer rounds while catching at least everything it catches today.

The product surface is governance text and one CLI validator. There is no user-facing screen or
component under `apps/` or `libs/` that renders to an end user, so the **UI-design-funnel is not
applicable** to this plan — the exemption is stated and justified in
[tech-docs.md §UI-Design-Funnel Exemption](./tech-docs.md#ui-design-funnel-exemption).

## Personas

Hats the solo maintainer wears, plus the agents that consume these surfaces.

| Persona                   | Description                                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Governance author**     | Changes a rule; needs to know the full blast radius before declaring the propagation complete    |
| **`repo-rules-maker`**    | Propagates a rule change; must start from the inbound-link set, not from the file it just edited |
| **`repo-rules-checker`**  | Validating agent; must sweep by stable key, record its scope, and argue against its own zero     |
| **`repo-rules-fixer`**    | Repairing agent; must sweep the whole class and re-check its own change surface for drift        |
| **Workflow orchestrator** | The calling context running the loop; needs a terminable stopping rule                           |
| **Maintainer**            | Reviews the resulting PR; needs sweep scope auditable without re-deriving it                     |

## User Stories

### US-1 — Blind-spot registry

As a **governance author**, I want a catalogue of the observed sweep blind spots with their git
proofs, so that I stop rediscovering the same structural search gaps on every rule change.

### US-2 — Mechanical never-touched detection

As the **workflow orchestrator**, I want the set of candidate files that no corrective commit has
touched computed mechanically, so that a sweep claiming completeness can be contradicted by
arithmetic rather than by another expensive semantic round.

### US-3 — Sweep by inbound link target

As **`repo-rules-checker`**, I want my primary sweep keyed on who links to the changed governing
document rather than on its phrasing, so that paraphrases and reverse-order prose stop escaping.

### US-4 — Auditable sweep scope

As the **maintainer**, I want every sweep to record its verbatim command and exclusion set in the
report, so that a claim of "repo-wide" is falsifiable when I read it.

### US-5 — Bounded directory scoping

As the **maintainer**, I want directory-scoped sweeps rejected unless their exclusions are enumerated
and justified, so that a subtree-only sweep can never present itself as complete.

### US-6 — Evidence grounded in the mechanism

As **`repo-rules-checker`**, I want claims about mechanical behavior verified against the workflow,
hook or script file that implements it rather than against another document, so that documentation
drift cannot validate itself.

### US-7 — Validator invocation parity

As **`repo-rules-checker`**, I want any validator invocation cited as evidence to match the flags CI
uses, so that a bare invocation over the validator's own negative fixtures cannot manufacture work.

### US-8 — Self-inflicted drift check

As **`repo-rules-fixer`**, I want my own change surface re-checked for claims my earlier commits
falsified, so that the loop stops generating the drift it exists to remove.

### US-9 — Adversarial termination

As the **workflow orchestrator**, I want the checker to run one adversarial round against its own
zero, using the mechanical never-touched set as its agenda, so that termination reflects search
completeness rather than operator fatigue.

### US-10 — Completeness-diff against ground truth

As **`repo-rules-checker`**, I want every document that describes an enumerable ground truth checked
by enumerating that ground truth and diffing it against the document, so that omissions with no
matchable text and no inbound link stop being invisible.

### US-11 — Ground truth that is not a file on disk

As **`repo-rules-checker`**, I want the completeness-diff contract to name its ground-truth source
explicitly — including sources that are not files, such as `git branch -r` — so that an enumeration
validated only against the filesystem cannot report completeness it has not established.

### US-12 — Guards placed at the point of rewrite

As **`repo-rules-fixer`**, I want any guard protecting an invariant placed at the point where a
rewrite happens rather than in a section I reach only if I already suspected the hazard, so that no
entry path into the file can bypass it.

### US-13 — Guard verification by entry-path enumeration

As the **maintainer**, I want a guard verified by enumerating every way an agent enters the file and
checking each path hits the guard before rewriting, so that a section's claim to bind "every recipe"
is never accepted as evidence that it does.

### US-14 — Search-tool validity before a zero is trusted

As the **maintainer**, I want any sweep concluding "nothing found" to record its verbatim command,
leave stderr unsuppressed, and demonstrate a known-positive control returning non-zero, so that a
broken command cannot present itself as a clean result.

### US-15 — Evidence-based review-cycle termination

As the **workflow orchestrator**, I want the PR-review maker→fixer loop to terminate when a cycle
finds nothing new rather than after a fixed count, so that a loop still producing blocking defects
is not declared complete by arithmetic.

### US-16 — Verification prompts that license a negative finding

As the **maintainer**, I want a verification prompt to explicitly permit refuting the requester's
hypothesis, so that a "nothing found" verdict means the reviewer looked rather than agreed.

### US-17 — Merge preconditions gate on committed fixes

As the **maintainer**, I want merge preconditions to verify that every finding's fix is committed
and pushed rather than that its review thread is resolved, so that a resolved thread over an
uncommitted fix cannot present the PR as clean.

## Acceptance Criteria

Every scenario below binds to at least one RED delivery step in [delivery.md](./delivery.md).

### AC-1 — The registry exists and every entry carries a git-verifiable proof

```gherkin
Scenario: Blind-spot registry lists each class with a checkable commit proof
  Given the file repo-governance/development/quality/governance-sweep-blind-spots.md exists
  When a reader opens any registry entry
  Then the entry states the blind-spot symptom, its corrective commit SHA, the sweep form that misses it, and the sweep form that catches it
  And running "git show --name-only" against the cited SHA shows the files the prior sweep had missed
  And the entry names the stable key its catching form sweeps on
```

### AC-2 — The directory-scope blind spot is catalogued with its git proof

```gherkin
Scenario: A subtree-only sweep claiming repo-wide scope is catalogued
  Given the registry entry for the directory-scoped blind spot
  When the reader follows its cited proof
  Then the proof shows that .github/ and specs/ were first touched only by the final corrective commit of the archived chain
  And the entry names enumerated-exclusion reporting as the catching form
  And the entry records that eleven prior rounds asserted repo-wide scope without demonstrating it
```

### AC-3 — Never-touched candidates are computed mechanically

```gherkin
Scenario: The validator reports candidate files no corrective commit touched
  Given a fixture repository state with a changed governing document and a set of corrective commits
  When the deterministic sweep-completeness pass runs against that range
  Then the pass reports every candidate file that links to the governing document and appears in no corrective commit
  And the pass reports zero never-touched candidates once every such file has been touched
```

### AC-4 — Directory-scoped sweeps with unenumerated exclusions are flagged

```gherkin
Scenario: A sweep report claiming repo-wide scope while excluding a subtree is flagged
  Given a sweep report whose recorded command restricts the search to a single directory
  When the deterministic sweep-completeness pass evaluates the report
  Then the pass reports a finding stating the sweep is directory-scoped without an enumerated exclusion set
  And the finding names the excluded top-level paths it detected
  And a report whose exclusions are enumerated with justifications yields no finding
```

### AC-5 — The sweep transcript is required and recorded verbatim

```gherkin
Scenario: An audit report records its sweep command verbatim
  Given repo-rules-checker has completed a sweep for a governance change
  When the checker writes its audit report
  Then the report contains the verbatim sweep command it executed
  And the report contains the exclusion set applied, or an explicit statement that no exclusions were applied
  And a report lacking the sweep transcript is reported as an incomplete-evidence finding
```

### AC-6 — Inbound-link sweep is the primary method

```gherkin
Scenario: The checker sweeps by inbound link target before sweeping by phrasing
  Given a governance change to a document that other documents link to
  When repo-rules-checker determines its sweep surface
  Then the checker enumerates every document linking to the changed document as the primary sweep set
  And keyword phrasing search runs as a secondary lens over that set rather than as the primary selector
  And the audit report records both sweep sets separately
```

### AC-7 — Paraphrase survivors are caught by the stable-key sweep

```gherkin
Scenario: A stale passage containing none of the search keywords is caught
  Given a document that links to the changed governing document
  And that document states the superseded rule in wording sharing no keyword with the change
  When the inbound-link sweep evaluates that document
  Then the passage is surfaced for review because the document is in the sweep set
  And the finding records that keyword search would not have selected this document
```

### AC-8 — Mechanical claims are verified against the mechanism

```gherkin
Scenario: A doc claim about CI behavior is checked against the workflow file
  Given a governance document asserting how a CI gate or hook behaves
  When repo-rules-checker validates that assertion
  Then the checker reads the workflow, hook or script file that implements the behavior
  And the checker does not accept a second document restating the claim as verification
  And the audit report cites the implementing file and line as the evidence
```

### AC-9 — Validator invocations must match CI flags

```gherkin
Scenario: A bare validator invocation over negative fixtures is rejected as evidence
  Given a validator that CI invokes with exclusion flags for its own test fixtures
  When repo-rules-checker runs that validator to produce evidence
  Then the checker uses the same flags CI uses, or records an explicit justification for diverging
  And findings produced by an invocation that omits CI's exclusion flags without justification are rejected as unverified
  And the audit report records the exact invocation used
```

### AC-10 — Self-inflicted drift is re-checked

```gherkin
Scenario: The fixer re-checks its own change surface for claims it falsified
  Given repo-rules-fixer has applied corrective commits across several documents
  When the fixer completes its pass
  Then the fixer re-examines every document it changed for claims invalidated by its own edits
  And the fix report lists each self-inflicted drift site with its disposition
  And a claim falsified by an earlier commit in the same chain is reported rather than left standing
```

### AC-11 — Class-wide remediation rather than instance repair

```gherkin
Scenario: A finding instantiating a registry blind-spot class triggers a whole-class sweep
  Given the checker reports a finding that instantiates a registry blind-spot class
  When repo-rules-fixer remediates it
  Then the fixer enumerates every instance of that class across the sweep set in the same pass
  And the fix report lists each enumerated site with its disposition
  And no instance of that class remains unaddressed in the sweep set
```

### AC-12 — Termination requires an adversarial round

```gherkin
Scenario: A zero verdict is challenged before it is accepted
  Given a validation round reports zero threshold-level findings
  When the workflow evaluates termination
  Then the workflow runs one adversarial round whose agenda is the mechanical never-touched candidate set
  And the workflow reports pass only if that adversarial round also reports zero
  And the final report records the never-touched set that the adversarial round consumed
```

### AC-13 — An empty adversarial agenda is itself reported

```gherkin
Scenario: The adversarial round reports its agenda even when empty
  Given the mechanical never-touched candidate set is empty at termination
  When the adversarial round runs
  Then the round records the empty agenda explicitly in the final report
  And the report states the candidate-set derivation used, so an empty set can be distinguished from an unrun computation
```

### AC-14 — The falsified convergence claim is corrected, not deleted

```gherkin
Scenario: The convergence expectation reflects the archived evidence
  Given the pattern convention previously claimed convergence in 1-3 iterations with escalation after 5
  When a reader opens the revised convergence guidance
  Then the guidance describes the phased budget of a deterministic pass, a bounded semantic budget, and one adversarial round
  And the guidance cites the archived 13-round chain as the falsifying evidence
  And the bare 1-3 iteration claim is absent from the pattern convention and the workflow
```

### AC-15 — No existing check was removed

```gherkin
Scenario: The validation step inventory does not shrink
  Given the pre-change inventory of repo-rules-checker validation steps recorded in Phase 0
  When the post-change inventory is taken
  Then every pre-change validation step is still present
  And the post-change step count is greater than or equal to the pre-change count
```

### AC-16 — Bindings stay generated, never hand-edited

```gherkin
Scenario: Secondary harness bindings are regenerated from the primary binding
  Given the .claude/ agent definitions have been modified
  When npm run generate:bindings runs
  Then the .opencode/ and .amazonq/ artifacts reflect the .claude/ changes
  And the harness sync validation reports no drift
```

### AC-17 — Tri-repo propagation preserves rhino-cli byte identity

```gherkin
Scenario: The validator lands byte-identical across all three repositories
  Given the new validator has landed in ose-public
  When the change is propagated to ose-primer and ose-infra
  Then apps/rhino-cli is byte-identical across all three repositories
  And the Gherkin behavior tree under the rhino specs path is byte-identical across all three
```

### AC-18 — The three text-invisible classes are catalogued with inline evidence

```gherkin
Scenario: BS-13, BS-14 and BS-15 are registered with evidence that survives SHA loss
  Given the blind-spot registry contains entries BS-13, BS-14 and BS-15
  When a reader opens each of the three entries
  Then each entry states why no text search and no inbound-link sweep could reach the defect
  And each entry names completeness-diff against ground truth as its catching form
  And the BS-15 entry records that its ground truth is a set of git refs rather than a file on disk
  And each entry carries its inline evidence so it stays auditable after its commit SHA stops resolving
```

### AC-19 — Classes compose rather than partition

```gherkin
Scenario: The registry records that one defect can instantiate several classes
  Given the registry entry for BS-15
  When a reader follows its cross-references
  Then the entry records that BS-15 is simultaneously an instance of BS-11 self-inflicted drift
  And the registry states that entries are lenses rather than mutually exclusive categories
  And the registry instructs the reader to continue matching after the first class matches
```

### AC-20 — Completeness-diff names its ground-truth source

```gherkin
Scenario: A document describing an enumerable ground truth is diffed against it
  Given a governance or reference document that enumerates workflows, agents, branches or files
  When repo-rules-checker validates that document
  Then the checker enumerates the ground truth from its authoritative source rather than from prose
  And the audit report names the ground-truth source it enumerated
  And every member of the ground truth absent from the document is reported as a finding
  And a report whose ground-truth source is unnamed is itself an incomplete-evidence finding
```

### AC-21 — Ground truth that is not a file on disk is still enumerated

```gherkin
Scenario: A rule scoped by an enumeration of git refs is checked against the refs
  Given a safety rule whose scope is an enumeration of environment branches
  When the completeness-diff contract evaluates that rule
  Then the contract enumerates the branches from git rather than from the document's own table
  And every branch absent from the rule's enumeration is reported as uncovered by the rule
  And the finding names the enumeration that failed open rather than only the missing members
```

### AC-22 — Guards sit at the point of rewrite

```gherkin
Scenario: A guard protecting an invariant binds before any rewrite occurs
  Given a fixer recipe that rewrites a delivery step
  When the recipe is applied
  Then the guard protecting the invariant is stated at the point of rewrite within that recipe
  And the guard binds regardless of which finding type routed the fixer to that recipe
  And a recipe that rewrites a step without a co-located guard is reported as a finding
```

### AC-23 — Guard coverage is verified by enumerating entry paths

```gherkin
Scenario: Every entry path into a guarded file reaches the guard before rewriting
  Given a file containing a guard and several recipes reachable by distinct finding types
  When the guard's coverage is verified
  Then the verification enumerates every entry path into the file by finding type and step number
  And each enumerated entry path is traced to confirm it reaches the guard before any rewrite
  And a section's own claim to bind every recipe is not accepted as evidence of coverage
```

### AC-24 — A sweep's zero requires a working-tool proof

```gherkin
Scenario: A zero-result sweep is rejected unless its tool is demonstrated to work
  Given a sweep whose conclusion is that nothing was found
  When the report is evaluated as evidence
  Then the report contains the verbatim command with stderr unsuppressed
  And the command uses a form the search tool accepts rather than a rejected flag
  And the report contains a known-positive control probe for the same pattern returning non-zero
  And a zero without a passing control probe is reported as unverified rather than as a clean result
```

### AC-25 — Review cycles terminate on evidence, not on a count

```gherkin
Scenario: The review loop continues while cycles keep finding blocking defects
  Given a PR-review maker to fixer cycle has completed its configured number of cycles
  When the loop evaluates termination
  Then the loop continues while the most recent cycle produced any new blocking finding
  And the loop terminates only after a cycle that produced no new finding
  And the verification prompt for that cycle explicitly permits refuting the requester's hypothesis
```

### AC-26 — Merge preconditions verify committed fixes, not resolved threads

```gherkin
Scenario: A resolved thread over an uncommitted fix does not satisfy the merge precondition
  Given a review finding whose thread has been marked resolved
  When the merge preconditions are evaluated
  Then the precondition verifies the corresponding fix is committed and pushed to the PR branch
  And a resolved thread whose fix is absent from the pushed diff is reported as an unmet precondition
  And the count of unresolved threads is not accepted as evidence that findings were fixed
```

## Product Scope

### In scope

- The blind-spot class registry as a governance quality document
- A deterministic sweep-completeness validator with a Gherkin behavior tree, registered as a
  `repo-governance audit` category
- Inbound-link-primary sweep, sweep transcript, and enumerated-exclusion contracts
- Evidence-grounding and validator-flag-parity contracts
- Class-wide remediation and self-inflicted-drift re-check contracts
- Workflow termination rewrite with the adversarial round, plus the corrected convergence guidance
- The completeness-diff contract, including non-filesystem ground truth (DECISION 11)
- The guard-placement contract and entry-path verification (DECISION 9)
- The search-tool-validity contract with its control-probe requirement (DECISION 10)
- Evidence-based review-cycle termination and the committed-fix merge precondition (DECISIONs 12
  and 13) — two narrow edits to `repo-governance/workflows/pr/pr-review-quality-gate.md`
- Binding regeneration and tri-repo propagation

### Out of scope

- Revisiting the governance change that supplied the evidence
- The sibling `plan-quality-gate` loop (DECISION 6) and the other repo gates (DECISION 5)
- **The `pr-review-maker` `REQUEST_CHANGES` limitation (gap D2)** — filed as a follow-up during
  Knowledge Capture; its fix is a token/identity change, not a governance-text change. Reasoning
  recorded in DECISION 13.
- Any relaxation of a check, threshold or criticality level
- Retroactive re-sweeps of governance changes already landed

## Product Risks

| Risk                                                               | Severity | Handling                                                                                              |
| ------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------- |
| Never-touched set is too large to act on                           | High     | Scoped to candidate files by inbound/outbound link plus declared blast radius (tech-docs DD-3)        |
| Adversarial round degenerates into a formality                     | High     | Its agenda is the mechanical set, not free-form doubt; an empty agenda is reported explicitly (AC-13) |
| Validator false positives add noise                                | Medium   | Existing FALSE_POSITIVE skip-list machinery applies; validator findings are checker-mediated          |
| Agent files grow past the instruction-size budget                  | Medium   | Registry content lives in the governance file; agents link rather than inline                         |
| Exclusion justifications become boilerplate                        | Low      | Exclusions recorded as literal globs, so the reviewer reads scope rather than prose about scope       |
| Tri-repo propagation partially applied, leaving repos inconsistent | Medium   | Per-repo phases with their own gates; byte-identity check is a gate item                              |
| Completeness-diff ground truth is unbounded or unnamed             | High     | Each contract instance names its authoritative source; an unnamed source is itself a finding (AC-20)  |
| Guard-placement rule read as "write more guards"                   | Medium   | Stated as the enumeration-fails-open rule with its four-failure evidence; AC-23 verifies entry paths  |
| Control probes become ceremonial and always pass trivially         | Medium   | The probe targets a known-positive control for the same pattern and tree (AC-24)                      |
| Evidence-based cycles never terminate on a noisy reviewer          | Medium   | Termination requires a cycle with no **new** finding; repeat findings do not extend the loop (AC-25)  |
| D2 review-state hole persists until its follow-up lands            | Medium   | Merge preconditions gate on finding text and committed diffs, never on GitHub review state (AC-26)    |
