Feature: Benchmark reference generation

  As a content maintainer
  I want the AI model benchmark reference tables to be regenerated from a single dataset
  So that docs/reference/ai-model-benchmarks.md never drifts from models.ts

  Background:
    Given a reference document with a roster generated block containing stale inner content

  @unit
  Scenario: Generate replaces only the inner text between a marker pair
    When the benchmark reference generator runs in generate mode
    Then the stale inner text should be replaced by the generated block

  @unit
  Scenario: Bytes outside the markers are preserved byte-for-byte
    When the benchmark reference generator runs in generate mode
    Then the lead-in and trailing prose should be unchanged
    And the BEGIN and END marker tags should remain in place

  @unit
  Scenario: A missing END marker throws under the marker-first guard
    Given a reference document whose roster block has a BEGIN marker but no END marker
    When the benchmark reference generator runs in generate mode
    Then it should throw an error naming the unclosed roster marker

  @unit
  Scenario: Generate mode is idempotent
    When the benchmark reference generator runs twice in generate mode
    Then the two outputs should be byte-identical with no duplicated content

  @unit
  Scenario: Validate mode exits non-zero on drift
    When the benchmark reference generator runs in validate mode
    Then it should detect drift and signal a non-zero exit
