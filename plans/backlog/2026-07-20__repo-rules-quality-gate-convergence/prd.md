# Product Requirements — Repo Rules Quality Gate Convergence

## Product Overview

Six coordinated changes to the repo-rules-quality-gate loop and its supporting agents, so the loop
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

## Product Scope

### In scope

- The blind-spot class registry as a governance quality document
- A deterministic sweep-completeness validator with a Gherkin behavior tree, registered as a
  `repo-governance audit` category
- Inbound-link-primary sweep, sweep transcript, and enumerated-exclusion contracts
- Evidence-grounding and validator-flag-parity contracts
- Class-wide remediation and self-inflicted-drift re-check contracts
- Workflow termination rewrite with the adversarial round, plus the corrected convergence guidance
- Binding regeneration and tri-repo propagation

### Out of scope

- Revisiting the governance change that supplied the evidence
- The sibling `plan-quality-gate` loop (DECISION 6) and the other repo gates (DECISION 5)
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
