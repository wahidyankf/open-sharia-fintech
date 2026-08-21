# Product Requirements — rhino-cli Governance Tooling Defects

## Product Overview

Three behaviour changes to `rhino-cli` governance commands, each making a currently-silent under-run
observable. No new command is introduced and no existing command is withdrawn.

## Personas

- **Governance maintainer** — edits `repo-governance/` prose and runs the pre-push gate. Needs the
  audit's verdict to be about the prose, not about how it happens to be wrapped.
- **Harness integrator** — adds or retires a coding-agent harness. Needs the registry to be the place
  that decision is expressed.
- **Sweep executor (human or AI)** — runs a bulk rename across a governed tree. Needs "matched
  nothing" to look different from "nothing needed changing".

## User Stories

- As a **governance maintainer**, I want the vendor audit to pair inline code spans across line
  breaks, so that reflowing a paragraph never invents or hides a finding.
- As a **harness integrator**, I want `harness bindings validate` to read its agent directories from
  the `harness:` registry, so that adding a harness is a config edit in one file rather than a Rust
  edit in four repositories.
- As a **sweep executor**, I want `readme-index rewrite-paths` to match full repo-relative paths, so
  that a directory rename is repointed rather than silently skipped.
- As a **sweep executor**, I want a rename map that matches no target to fail loudly, so that a typo
  in the map cannot masquerade as a completed sweep.
- As a **sweep executor**, I want tracked non-markdown files scanned for renamed governance paths, so
  that a stale path in a config comment is reported by a tool rather than by a manual `grep` months
  later.
- As a **plan executor baselining a repository**, I want `readme-index validate`'s verdict line to
  count only the findings that can fail the run, so that a dark-launched finding kind does not make
  a passing gate read as failing.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Vendor audit pairs inline code spans across line wraps

  Scenario: A code span straddling a line break is still treated as code
    Given a governance markdown file whose inline code span "`harness bindings generate`"
      is wrapped across two lines
    And the following line contains "`.claude/`" inside backticks
    When I run "repo-governance vendor validate"
    Then no finding names ".claude/"
    And the exit code is 0

  Scenario: Rejoining the span does not change the verdict
    Given the same file with the code span rejoined onto one line
    When I run "repo-governance vendor validate"
    Then the finding set is byte-identical to the wrapped variant's finding set

  Scenario: A genuine bare-prose vendor term is still reported
    Given a governance markdown file with a wrapped code span
    And a later line naming ".claude/" outside any code span
    When I run "repo-governance vendor validate"
    Then a finding names ".claude/"
    And the exit code is non-zero
```

```gherkin
Feature: harness bindings validate derives agent directories from the registry

  Scenario: A harness whose agent directory is not .claude/agents
    Given a repository whose "harness:" registry declares a primary tier at ".custom-src/agents"
    And that directory holds one agent file with a synchronized mirror
    When I run "harness bindings validate"
    Then the exit code is 0
    And no output names ".claude/agents"

  Scenario: Mirror drift is still detected under a non-default source directory
    Given the same repository
    And the mirror's content differs from its source
    When I run "harness bindings validate"
    Then the exit code is non-zero
    And a finding names the drifted mirror

  Scenario: The registry is the only place a new harness is declared
    Given a repository with a twelfth agent-bearing harness added to "harness:" only
    When I run "harness bindings validate"
    Then the new harness's directory is included in the validated set
```

```gherkin
Feature: readme-index rewrite-paths matches repo-relative paths

  Scenario: A directory rename is repointed
    Given a rename map row "repo-governance/a/01-x/ -> repo-governance/a/x/"
    And a markdown file linking to "repo-governance/a/01-x/leaf.md"
    When I run "governance readme-index rewrite-paths --map <map>"
    Then the link target becomes "repo-governance/a/x/leaf.md"

  Scenario: Two files sharing a basename in different directories are disambiguated
    Given a rename map naming only "docs/a/leaf.md"
    And a second file "docs/b/leaf.md" that is not in the map
    When I run "governance readme-index rewrite-paths --map <map>"
    Then links to "docs/a/leaf.md" are repointed
    And links to "docs/b/leaf.md" are unchanged

  Scenario: A map that matches nothing fails loudly
    Given a rename map whose every row names a path present in no tracked file
    When I run "governance readme-index rewrite-paths --map <map>"
    Then the exit code is non-zero
    And the output states how many map rows matched no target

  Scenario: An empty map is not an error
    Given a rename map containing only comments and blank lines
    When I run "governance readme-index rewrite-paths --map <map>"
    Then the exit code is 0

  Scenario: The verdict line counts only findings that can fail the run
    Given a tree producing 3 "unannotated" findings and no other kind
    When I run "governance readme-index validate" with no "--fail-kinds"
    Then the exit code is 0
    And the verdict line reports 0 failing findings and 3 informational ones
    And all 3 findings are still listed individually

  Scenario: Arming a dark-launched kind makes it count in both signals
    Given a tree producing 3 "unannotated" findings and no other kind
    When I run "governance readme-index validate --fail-kinds unannotated"
    Then the exit code is non-zero
    And the verdict line reports 3 failing findings

  Scenario: A kind that always gates is unaffected
    Given a tree producing 1 "ghost" finding
    When I run "governance readme-index validate" with no "--fail-kinds"
    Then the exit code is non-zero
    And the verdict line reports 1 failing finding

  Scenario: A renamed governance path inside a tracked non-markdown file is repointed
    Given a rename map row "repo-governance/a/01-x.md -> repo-governance/a/x.md"
    And a tracked ".gitignore" whose comment names "repo-governance/a/01-x.md"
    When I run "governance readme-index rewrite-paths --map <map> --include-non-markdown"
    Then the comment names "repo-governance/a/x.md"
    And no binary file is modified
```

## In Scope

- Document-level inline-code-span pairing in the vendor audit's prose stripper.
- Registry-derived agent directory resolution in `harness bindings validate`.
- Repo-relative path matching, a no-match failure signal, and opt-in non-markdown rewriting in
  `readme-index rewrite-paths`.
- A `readme-index validate` verdict line derived from the same `--fail-kinds` filter as its exit
  code, distinguishing failing findings from informational ones.
- Companion Gherkin under `specs/apps/rhino/behavior/rhino-cli/gherkin/`.
- Parity manifest regeneration in each source-changing commit.

## Out of Scope

- Fenced code **blocks** (triple-backtick) in the vendor audit — already handled; only inline spans
  reset per line.
- Any change to which vendor terms the audit checks.
- Restoring either withdrawn naming validator.
- Rewriting binary files, or any file not tracked by git.
- General non-markdown link health.
- Changing which kinds gate by default. `unannotated` stays dark-launched; WS-4 changes only how the
  verdict is worded, never which findings fail a run.
- Fixing the 425 `unannotated` findings themselves — 163 in `docs/`, 262 in `specs/`. That is
  content work under whichever plan owns those trees, not a tooling defect.

## Product Risks

| Risk                                                                                          | Severity | Note                                                                                                              |
| --------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| Document-level pairing changes findings on the existing corpus.                               | Medium   | Golden-master the current finding set first; every delta is reviewed before the fix lands.                        |
| Non-markdown rewriting corrupts a file with an unusual encoding.                              | Medium   | Opt-in flag, tracked text files only, skip anything with a NUL byte, and assert byte-identity on untouched files. |
| A stricter exit code on no-match breaks an existing caller.                                   | Low      | Enumerate callers before the change; `rewrite-paths` is not currently wired into any gate surface.                |
| Registry-derived directories change which files `bindings validate` walks in this repository. | Low      | The resolved set must be asserted equal to today's set for this repository's real layout.                         |
