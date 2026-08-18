# 📚 Product Requirements: Repository Clean-Up

## Overview

The product here is the contributor experience of the repository itself: what a person finds when
they look for link validation, and whether what they find works.

## Personas

| Persona                   | Context                                                                               | What they need                                                   |
| ------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Content author**        | Writes or edits Markdown under `apps/ayokoding-www/content` or `apps/ose-www/content` | To be told before merge if a link they wrote points nowhere.     |
| **Repository maintainer** | Bumps toolchains, audits dependencies, runs lint sweeps across every project          | To not spend that effort on projects nothing executes.           |
| **New contributor**       | Reads `repo-governance/` and `docs/` to learn how the repo validates itself           | Every documented command to work when run, first time.           |
| **AI agent**              | Loads `.claude/skills/` reference files as instructions                               | Those instructions to describe the repository as it actually is. |

## User Stories

- As a **content author**, I want broken links in the content trees to fail a gate, so that a dead
  cross-reference is caught in CI instead of by a reader.
- As a **repository maintainer**, I want dormant projects removed, so that toolchain and dependency
  work is spent only on code that runs.
- As a **new contributor**, I want the link-validation documentation to name a command that exists,
  so that following the governance surface does not teach me to distrust it.
- As an **AI agent**, I want `.claude/skills/` reference files to state the current validation
  route, so that I do not skip the content trees on the strength of a stale note.

## Acceptance Criteria

```gherkin
Feature: Content link validation coverage

  Scenario: A broken content link fails the gate
    Given the md-links gate carries no content-tree exclusions
    When a Markdown file under apps/ayokoding-www/content links to a file that does not exist
    Then "md links validate" exits non-zero
    And the report names that file and line

  Scenario: The content trees pass today
    Given the single pre-existing broken link has been retargeted
    When "md links validate --exclude plans/done" runs
    Then it exits 0
    And it reports no broken links

Feature: Retired projects leave no trace

  Scenario: No documented command names a deleted target
    Given ayokoding-cli, ose-cli, rust-commons, and beavernest-app-web are deleted
    When the repository is searched outside plans/done, apps/*/content, and social-media-posts
    Then no file names any of those four projects

  Scenario: The surviving projects are unaffected
    Given the dead links:check target and both implicitDependencies are removed
    When "nx run-many -t test:quick -p ayokoding-www,ose-www,beavernest-app,beavernest-be" runs
    Then every project passes

Feature: Governance documentation is executable

  Scenario: Every documented command runs
    Given the documentation sweep is complete
    When each command shown in repo-governance/ and docs/ for link validation is executed
    Then each exits 0
```

## Product Scope

**In scope**: removing the four retired projects and every live reference to them; arming `md-links`
on both content trees; correcting the two `.claude/skills/` reference files and regenerating their
harness mirrors.

**Out of scope**: changing how `md links validate` reports; anchor-level link validation; `crane-cli`;
`rhino-cli` behaviour; content rewriting beyond the single broken link.

## Product Risks

| Risk                                                                       | Mitigation                                                                                                          |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| A contributor's in-flight branch touches a deleted path                    | The deletions are dormant code; no branch can be running them. Merge conflicts surface normally.                    |
| Arming the gate surfaces links that drift in between measurement and merge | Phase 3 re-measures rather than trusting the recorded count, and the gate runs on the PR's merge commit.            |
| The documentation sweep misses a surface                                   | The Definition-of-Done check is a whole-repo grep with a zero-outside-historical-roots acceptance, not a file list. |
| Regenerated harness mirrors drift from `.claude/`                          | `npm run validate:sync` gates the same commit; mirrors are never hand-edited.                                       |
