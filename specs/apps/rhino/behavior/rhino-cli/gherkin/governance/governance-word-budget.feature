@governance-word-budget
Feature: Governance word budget

  As an AI coding agent
  I want every governance file kept under a word ceiling
  So that I can hold the whole rule in context without silent truncation

  Background:
    Given repo-config.yml declares a governance-word-budget section
    And the section sets target 650, warn 750, fail 750

  Scenario: A file within target passes silently
    Given "repo-governance/conventions/formatting/linking.md" contains 650 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output contains no finding for that file

  Scenario: A file between target and fail warns without blocking
    Given "repo-governance/conventions/formatting/linking.md" contains 750 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output contains a "warn" finding naming that file

  Scenario: A file over the ceiling fails the gate
    Given "repo-governance/development/agents/ai-agents.md" contains 14720 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the output contains a "fail" finding naming that file
    And the finding states the word count 14720 and the ceiling 750
    And the finding links the governance word budget convention

  Scenario Outline: Every covered surface is scanned
    Given a file "<path>" contains 900 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the output contains a "fail" finding naming "<path>"

    Examples:
      | path                                     |
      | repo-governance/principles/example.md    |
      | .claude/agents/example.md                |
      | .claude/skills/example/SKILL.md          |
      | .opencode/agents/example.md              |
      | .codex/agents/example.md                 |
      | .agents/skills/example/SKILL.md          |
      | AGENTS.md                                |
      | CLAUDE.md                                |
      | RTK.md                                   |

  Scenario: The covered surfaces are exactly the live entry points of the supported harnesses
    When I read repo-config.yml
    Then the covered surface globs are exactly the harness entry points and the README glob
    And the README glob is declared last

  Scenario: A configured glob matching no file is a no-op
    Given no file exists at ".codex/agents/example.md"
    When the developer runs governance word-budget validate
    Then no finding is emitted for ".codex/agents/example.md"

  Scenario Outline: A root entry point uses the ordinary 750-word ceiling
    Given a file "<path>" contains 751 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the output contains a "fail" finding naming "<path>"
    And the finding states the word count 751 and the ceiling 750

    Examples:
      | path      |
      | AGENTS.md |
      | CLAUDE.md |

  Scenario: A README.md file under the specific-surface target produces zero findings
    Given "repo-governance/development/quality/README.md" contains 900 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output contains no finding naming that file
    And this holds even though 900 words exceeds the general surface's 750-word fail ceiling, because the winning README-specific surface classifies 900 words as "ok" against its own 900-word target

  Scenario: A README.md file uses the wider README-specific glob threshold
    Given "repo-governance/development/quality/README.md" contains 1000 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output contains a "warn" finding naming that file, not a "fail" finding

  Scenario: A README.md file over the wider ceiling still fails
    Given "repo-governance/development/quality/README.md" contains 1001 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the output contains a "fail" finding naming that file

  Scenario: Non-prose content counts toward the budget
    Given "repo-governance/conventions/formatting/diagrams.md" contains 200 prose words
    And it contains a Mermaid block of 600 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the reported word count is 800

  Scenario: An out-of-scope file is never scanned
    Given "apps/ayokoding-www/content/lesson.md" contains 5000 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output contains no finding for that file

  Scenario: The config schema rejects an exemption key
    Given repo-config.yml adds "exempt: [AGENTS.md]" under governance-word-budget
    When the developer runs repo-config schema validate
    Then the command exits with a failure code

  Scenario: The old command is gone
    When the developer runs harness instruction-size validate
    Then the command exits with a usage error
    And the output reports an unknown subcommand

  Scenario: The old config block is gone
    When I read repo-config.yml
    Then it contains no "instruction-size:" section
    And it contains a "governance-word-budget:" section

  Scenario: The old gate id is replaced by the armed word-budget gate
    When the developer runs gate list with surface pre-push and format text
    Then the output contains no gate id "instruction-size"
    And the output contains gate id "governance-word-budget"

  Scenario: The resolved tree is measured in words
    Given "CLAUDE.md" contains 480 words
    And "CLAUDE.md" imports "AGENTS.md" via an @-directive
    And "AGENTS.md" contains 490 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the reported resolved-tree word count is 970

  Scenario: An oversized resolved tree fails
    Given the resolved CLAUDE.md tree totals 1600 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the output contains a "fail" finding for the resolved tree

  Scenario: Import cycles terminate
    Given "CLAUDE.md" imports "AGENTS.md"
    And "AGENTS.md" imports "CLAUDE.md"
    When the developer runs governance word-budget validate
    Then the command terminates
    And each file is counted at most once

  Scenario: A generated mirror is still subject to the word budget
    Given ".opencode/agents/plan-checker.md" contains 900 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the finding names ".opencode/agents/plan-checker.md"

  Scenario: No inbound link to the renamed convention is left broken
    When the developer runs md links validate
    Then the command exits successfully
