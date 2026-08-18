# Product Requirements — File Naming Convention Rework

## Product Overview

Prose changes to two governance conventions, propagated across every surface that restates them, plus
one code change (WS-B3) to the word-budget remediation emitter so it cannot produce colliding names.

## Personas

- **Contributor naming a new file** — reads `file-naming.md` once and expects the gate to agree.
- **Auditor** — compares the convention against the tree and needs the comparison to be decidable.
- **Sweep executor** — needs a verdict for the hard cases before the sweep, not discovered mid-run.
- **Shard author** — splits an oversized document and must not create a collision by doing so.

## User Stories

- As a **contributor**, I want every exempt filename named in the convention, so that I do not have to
  read Rust to know whether my file is governed.
- As a **contributor**, I want `_index.md` documented as an exception, so that the "no underscores"
  rule and the content trees stop contradicting each other.
- As an **auditor**, I want the convention's scope stated as an evaluable path expression, so that
  "does this rule cover this file?" has one answer.
- As an **auditor**, I want the convention to say which extensions are actually enforced, so that a
  `.svg` name is not assumed to be gated when it is not.
- As a **sweep executor**, I want the ordinal convention's worked-cases table to agree with its own
  normative sentence, so that the hard case I look up is not the one that is wrong.
- As a **sweep executor**, I want a stated verdict for basenames that differ only by ordinal, so that
  the same rule produces the same outcome in both repositories.
- As a **shard author**, I want the split tool to refuse to emit two names differing only by ordinal,
  so that the collision class stops growing.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: The convention's exemption list matches the enforced one

  Scenario: Every gate-exempt basename is documented
    Given the set of basenames exempted by "md naming validate" in source
    And the set of exempt globs in the "md-naming" gate registry entry
    When I compare them against the exceptions named in "file-naming.md"
    Then every enforced exemption appears in the convention
    And every convention-stated exemption is enforced

  Scenario: An exemption states why it exists
    Given the convention's exceptions section
    When I read any exemption entry
    Then it names the external requirement that mandates the fixed filename
```

```gherkin
Feature: The convention's scope is evaluable

  Scenario: Scope is stated as a path expression
    Given "file-naming.md"
    When I read its scope clause
    Then it states a path set that can be evaluated against the tree
    And it does not use an open-ended qualifier such as "and similar locations"

  Scenario: Enforced extensions are distinguished from governed ones
    Given the convention's extension list
    When I read it
    Then it states which extensions the gate actually validates
    And it states that the remainder are convention-only
```

```gherkin
Feature: The ordinal convention does not contradict itself

  Scenario: No worked-case row contradicts the normative rule
    Given the worked-cases table in "ordinal-filename-prefixes.md"
    When I evaluate each row's verdict against the rule stated above the table
    Then no row's verdict disagrees with the rule
    And the step-range clause is stated before the row that depends on it

  Scenario: The keep-clause non-vacuity check still passes
    Given each repository's copy of the convention
    When I run the non-vacuity command it publishes
    Then the command runs without error
    And its result matches what that copy of the convention claims
```

```gherkin
Feature: Basenames differing only by ordinal have a stated verdict

  Scenario: The convention rules on the collision case
    Given two governed filenames whose stems are identical and whose ordinals differ
    When I consult "ordinal-filename-prefixes.md"
    Then it states whether the ordinal is kept, and why
    And it states what to do instead when the stem is a truncation artifact

  Scenario: The split emitter refuses to create a collision
    Given a document split that would emit "04-<stem>.md" and "05-<stem>.md" with identical stems
    When the remediation tool runs
    Then it fails with a message naming both candidate filenames
    And no file is written
```

## In Scope

- `repo-governance/conventions/structure/file-naming.md` and
  `ordinal-filename-prefixes.md`, in both repositories, plus any child shard the word budget forces.
- Every rules-machinery surface restating either rule: `repo-rules-checker`, `repo-rules-fixer`,
  `repo-rules-maker`, the `repo-validating-governance-rules` and `repo-rules-fixing` skills, and the
  `repo-rules-quality-gate` workflow shards.
- The `md-naming` gate registry entry, if the reconciliation shows a redundant or wrong glob.
- The word-budget remediation emitter's collision refusal (WS-B3, the only code change).

## Out of Scope

- Renaming any existing file, including the 40 collision files.
- Widening `md naming validate` to non-`.md` extensions.
- Restoring either withdrawn naming rule.
- Any change to the kebab-case charset itself.

## Product Risks

| Risk                                                                            | Severity | Note                                                                                                      |
| ------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------- |
| Both conventions exceed the 500-word budget once the missing content is added.  | High     | Near the cap already. Plan a child shard from the start rather than discovering the overflow mid-edit.    |
| A worked-case verdict change silently changes what a future sweep would rename. | Medium   | Evaluate every changed verdict against the current tree and state the affected file count before landing. |
| The emitter's collision refusal blocks a legitimate split.                      | Medium   | Refuse with both candidate names in the message so the author can supply distinct stems immediately.      |
| The two repositories' conventions diverge again.                                | Medium   | One delivery unit covers both; per-repository facts are re-derived by command, never copied.              |
