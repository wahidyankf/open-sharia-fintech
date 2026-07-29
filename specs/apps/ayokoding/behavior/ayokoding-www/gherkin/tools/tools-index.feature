Feature: Tools index

  # AC-13 (UWT-009) — The tools index calculator entry has a description distinct from its link text
  @unit @e2e
  Scenario: The calculator entry shows a description distinct from its link text
    Given I am on the tools index page
    When the calculator entry renders
    Then the calculator entry shows a description distinct from its link text

  # AC-3 — Phase 10 reveal: the AI benchmark tool gets its own tools-index entry
  @unit @e2e
  Scenario: The AI benchmark entry shows a description distinct from its link text
    Given I am on the tools index page
    When the AI benchmark entry renders
    Then the AI benchmark entry shows a description distinct from its link text
