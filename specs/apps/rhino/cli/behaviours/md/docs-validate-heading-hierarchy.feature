@docs-validate-heading-hierarchy
Feature: Docs Markdown Heading Hierarchy Validation

  As a repository maintainer
  I want to scan documentation directories for markdown files that violate the
  heading hierarchy rule (exactly one H1, no skipped levels)
  So that markdown content stays accessible to screen readers and renderers
  that depend on a well-formed outline

  Scenario: Tree where every .md has exactly one H1 and no skipped levels passes
    Given a documentation tree where every markdown file has exactly one H1 and no skipped heading levels
    When the developer runs docs validate-heading-hierarchy
    Then the command exits successfully
    And the output reports zero docs heading hierarchy findings

  Scenario: File with two H1 headings fails
    Given a documentation tree containing a markdown file with two H1 headings
    When the developer runs docs validate-heading-hierarchy
    Then the command exits with a failure code
    And the output identifies the offending file and the duplicate H1 violation

  Scenario: File with H2 followed directly by H4 (skipping H3) fails
    Given a documentation tree containing a markdown file with an H2 followed directly by an H4
    When the developer runs docs validate-heading-hierarchy
    Then the command exits with a failure code
    And the output identifies the offending file and the skipped heading level

  Scenario: Single-line file with no headings is ignored (passes)
    Given a documentation tree containing a single-line markdown file with no headings
    When the developer runs docs validate-heading-hierarchy
    Then the command exits successfully
    And the output reports zero docs heading hierarchy findings

  Scenario: prose-allowlist-runs — docs file triggers a heading finding
    Given a docs directory containing a markdown file with two H1 headings
    When the developer runs docs validate-heading-hierarchy
    Then the command exits with a failure code
    And the output identifies the duplicate H1 violation in the docs file

  Scenario: agent-skill-file-exempt — no finding for agent or skill files
    Given a .claude/agents directory containing a markdown file with no H1 heading
    When the developer runs docs validate-heading-hierarchy
    Then the command exits successfully
    And the output reports zero docs heading hierarchy findings

  Scenario: plans-done-excluded — no finding for plans/done files
    Given a plans/done directory containing a markdown file with a skipped heading level
    When the developer runs docs validate-heading-hierarchy
    Then the command exits successfully
    And the output reports zero docs heading hierarchy findings

  Scenario: exclude-flag-suppresses-tree — --exclude docs suppresses docs findings
    Given a docs directory containing a markdown file with two H1 headings
    And a repo-governance directory containing a markdown file with two H1 headings
    When the developer runs docs validate-heading-hierarchy with --exclude docs
    Then the command exits with a failure code
    And the output does not mention the docs file
    But the output identifies the repo-governance file

  Scenario: specs-allowlisted — specs tree triggers a heading finding
    Given a specs directory containing a markdown file with two H1 headings
    When the developer runs docs validate-heading-hierarchy
    Then the command exits with a failure code
    And the output identifies the duplicate H1 violation in the specs file

  Scenario: app-readme-allowlisted — project-root README triggers a heading finding
    Given an apps/example directory whose README.md contains a skipped heading level
    When the developer runs docs validate-heading-hierarchy
    Then the command exits with a failure code
    And the output identifies the skipped heading level in the app README

  Scenario: app-internals-default-deny — deep app files yield no finding
    Given an apps/example/src directory containing a markdown file with no H1 heading
    When the developer runs docs validate-heading-hierarchy
    Then the command exits successfully
    And the output reports zero docs heading hierarchy findings

  Scenario: project-docs-subtree-allowlisted — app and lib docs trees trigger findings
    Given a libs/example/docs directory containing a markdown file with two H1 headings
    When the developer runs docs validate-heading-hierarchy
    Then the command exits with a failure code
    And the output identifies the duplicate H1 violation in the lib docs file
